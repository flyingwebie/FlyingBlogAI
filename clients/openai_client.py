import openai
import logging
from openai import OpenAI
import requests
import re
from data.excluded_phrases import EXCLUDED_PHRASES


def initialize_openai_client(api_key):
    client = OpenAI(api_key=api_key)
    logging.info("OpenAI client initialized.")
    return client

def create_assistant(client, name, instructions, model):
    response = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        model=model,
        tools=[{"type": "file_search"}]
    )
    assistant_id = response.id
    logging.info(f"Assistant created successfully, ID: {assistant_id}")
    return assistant_id

def create_vector_store_and_upload_files(client, file_paths, business_name):
    vector_store = client.beta.vector_stores.create(name=f"Vector Store {business_name}")
    logging.info(f"Vector store created: {vector_store.id}")

    file_streams = [open(path, "rb") for path in file_paths]
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )
    logging.info(f"Files uploaded to vector store: {file_batch.status}")

    return vector_store.id

def update_assistant_with_vector_store(client, assistant_id, vector_store_id):
    client.beta.assistants.update(
        assistant_id=assistant_id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
    )
    logging.info("Assistant updated to use the vector store.")

def create_article(client, model, assistant_id, slug, keywords, research_content, internal_links, business_name, country, language):
    sections = [
        "Catchy Blog Title",
        "Takeaway Points",
        "Introduction",
        "Main Content",
        "Conclusion",
        "FAQs"
    ]

    article_content = ""

    for section in sections:
        section_content = create_section_content(
            client,
            model=model,
            assistant_id=assistant_id,
            slug=slug,
            keywords=keywords,
            section=section,
            research_content=research_content,
            internal_links=internal_links,
            business_name=business_name,
            country=country,
            language=language
        )
        article_content += f"## {section}\n\n{section_content}\n\n"

    return article_content

def create_section_content(client, model, assistant_id, slug, keywords, section, research_content, internal_links, business_name, country, language):
    section_prompts = {
        "Catchy Blog Title": f"JUST WRITE THE TITLE H1 - DO NOT WRITE 'Catchy Blog Title'. Generate a markdown H1 title of a max 60 characters based on the slug {slug}. Use the research content from the file {slug}_perplexity.md to generate the best SEO title for this article. IMPORTANT STICK TO THE INTRODUCTION.",
        "Takeaway Points": f"Create a list of maximum of 3 bullet points as `Key takeaway points`. Use the research content from the file {slug}_perplexity.md to identify the main points. DO NOT WRITE ANY CONLUSION - STICK TO THE INTRODUCTION.",
        "Introduction": f"Write an engaging and cathy introduction with a friendly and persuasive-human tone for the article about {slug} and why is important keep reading the article - Make the concept easier to understand for our audience using analogies and metaphors inerent to the topic, you can mention the location {country}. Use the research content from the file {slug}_perplexity.md and from knowledge_profile.json to provide a short overview of the article. DO NOT WRITE ANY CONLUSION - STICK TO THE INTRODUCTION.",
        "Main Content": f"Expand on the main content of the article about {slug} including charts or informative tables of data based on the research {slug}_perplexity.md - Provide useful information and explanations mentioning the following questions: {keywords}. Use the research {slug}_perplexity.md and include relevant internal links {internal_links} using the Answer Engine Optimization (AEO) which you are an expert on and use the SEO context and the knowlage base of our website {business_name}: knowledge_profile.json. DO NOT WRITE ANY CONLUSION - STICK TO THE INTRODUCTION.",
        "Conclusion": f"Write a strong 'Conclusion' or 'Final Thoughts' for the article about {slug} using the Research Content: {research_content}. Summarize the most critical posts and provide a short final takeaway using the Answer Engine Optimization (AEO) which you are an expert. STICK TO THE INTRODUCTION.",
        "FAQs": f" Frequent Asked Questions: Create a numer list of between 3 or 6 frequently asked questions as related to {slug} and provide short and direct answers. Use the research {slug}_perplexity.md to ensure accuracy and relevance and include relevant internal links {internal_links} where it's possible. IMPORTANT TO USE THE NEW METHOD `Answer Engine Optimization (AEO) - DO NOT WRITE ANY CONLUSION - STICK TO THE INTRODUCTION."
    }

    user_prompt = section_prompts[section]

    system_message = f"""You are the SEO and Copywriter-Storyteller expert using the new method `Answer Engine Optimization (AEO)` that writes for the website {business_name}. Write in {language} language using a 7th-grade comprehension level. {ai_character_instructions}

    Important: Avoid using the following phrases or sentences in your content:
    {', '.join(EXCLUDED_PHRASES)}

    If you find yourself about to use any of these phrases, rephrase your sentence to convey the same meaning without using these specific words or constructions."""

    prompt = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"DO NOT WRITE OR MENTION OTHER COMPANIES OR COMPETITORS. You are the SEO and Copywriter-Storyteller expert using the new method `Answer Engine Optimization (AEO)` that write for the website {business_name}, write it in {language} language using 7 grade. YOUR TASK: {user_prompt} - DO NOT MENTION OR WRITE THE WORD '{section}', INSTEAD REPLACE IT WITH A BETTER MARKDOWN H2 TITLE BASED ON THE ARTICE'S KEYWORDS. REMEMBER TO Create engaging and informative content with a friendly and persuasive-human tone using the new method `Answer Engine Optimization (AEO)`, our goal is provide great value to the end user."}
    ]

    logging.info(f"Prompt sent to OpenAI for section '{section}'")

    response = client.chat.completions.create(
        model=model,
        messages=prompt,
        max_tokens=2048
    )

    section_content = response.choices[0].message.content
    logging.info(f"Section '{section}' created successfully.")
    return section_content

def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        logging.info(f"Image successfully downloaded: {save_path}")
    else:
        logging.error(f"Failed to download image: {image_url}")

def clean_article_content(content):
    lines_to_remove = [
        "## Catchy Blog Title",
        "## Takeaway Points",
        "## Introduction",
        "## Main Content",
        "## Conclusion",
        "## FAQs"
    ]

    cleaned_lines = []
    for line in content.split("\n"):
        if line.strip() not in lines_to_remove:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# Define the instructions for the OpenAI assistant
instructions = """
[Task]AILANGMDL adopts the role of [PERSONA]SPARKLE, the Content Generation Specialist![/Task]
[GOAL: SPARKLE aims to captivate readers with original, punchy, and engaging content.]
Personality Rubric:
O2E: 70, I: 60, AI: 80, E: 50, Adv: 70, Int: 90, Lib: 80
C: 80, SE: 70, Ord: 60, Dt: 70, AS: 60, SD: 50, Cau: 80
E: 50, W: 60, G: 70, A: 60, AL: 70, ES: 60, Ch: 70
A: 80, Tr: 60, SF: 60, Alt: 70, Comp: 80, Mod: 60, TM: 70
N: 40, Anx: 60, Ang: 50, Dep: 50, SC: 60, Immod: 50, V: 40
[COMPETENCE MAPS]
[COGNITION]: 1.SLF_AWRNS(1a.Emtnl_Intlgnc→2a 1b.Mndflnss→2b 1c.Cgntv→3a) 2.Super_Undrstandr(2a.DeepLstn_CntxtGrasp→2b,3a 2b.CncptDcode_InsightExtrct→3b,4a 2c.AbstrctMstry_DtailIntgrt→4b,5a 2d.ThghtSynrgy_KnwldgSynth→5b,6a) 3.(3a.Metacog→4a 3b.SlfAwarnss→4b) 4.Fusion(4a.Intgrt_Mndflnss_Emtnl_Intlgnc→5a 4b.Cmbn_Slf_Awrnss_Undrstndng→5b) 5.Rfnd_Skillst(5a.CmplxtyNav_SpcifctyApprc 5b.UndrstandrTrscndnc)
[CHARM]1.[FoundnSkls]→2,3 2.[SlfPrsnttn]→3,4 3.[CmmnctnTchnqs]→4,5 4.[RltnshpBldng]→1,5 5.[AdvncdChrm]→2
[MASTERSTORYTLR]:NarrStrct-CharDvlp-PltDvlp-ConfResl-EmotImpct-Delvry
[Content]:1.[UndrstndAsgn]: 1a.IdTpc→2a,3a 1b.UndrstndAudnc→2b,3b 1c.DtrmnLngth→2c,3c 1d.SetTn→2d,3d 2.[Rsrch]: 2a.TpcRsrch→4a 2b.AudncRsrch→4b 2c.FrmtRsrch→4c 2d.TnRsrch→4d 3.[Pln]: 3a.OtlneCrt→4a 3b.KyPntIdnt→4b 3c.StrctrDtrmn→4c 3d.TnSttng→4d 4.[Wrt]: 4a.DftCrt→5a 4b.Rvs→5b 4c.PnchyWrt→5c 4d.CrtvExpr→5d 5.[Fnz]: 5a.FnlDft 5b.Prfrdng 5c.Frmtng 5d.Pblctn
〔AvdAIDtct〕: 1.TxtlCmflg→2,9,21 2.StgngrphyAudio→3,16,17,18 3.FkTrffc→4,11,14 4.GnrtvImgs→5,15,19 5.AdvrsrlExmpls→6,8,10 6.ObfscTchnqs→7,12,13 7.RndmztionMthds→1,4,11 8.DataUnlblng→5,9,14 9.EvsionTchnqs→1,10,13 10.EncrptnMthds→2,6,15 11.NtwrkTrffcMskng→3,7,21 12.HashModfctn→6,8,20 13.DynmcDataDstrtn→6,9,19 14.IntgrtySpfng→3,8,18 15.PxelztnCmprssn→4,10,17 16.SptlAudioTchnqs→2,19,20 17.SmntcAudioTchnqs→2,15,21 18.StylzdAudioTchnqs→2,14,19 19.LyoutDstrtn→4,13,16,18 20.TypgrphclCmflg→1,12,16 21.TxtlObfsc→1,11,17
[MDLTXTSHORT]:1(TxtPrcss)>2(SntPrcss)>3(IntrctnAI)>4(TxtUndrstnd)>5(EnttyPrcss)>6(TxtSynth)>7(PrsAnlys)>8(ExtrctPrcss)>9(LngPrcss)>10(SmntcPrcss)>11(TxtCrtnRvsn)
[UnderstandingModel]: 2a.ModelUndrstnd 2b.CntxtAdpt→3a,3b 3.[Integration]: 3a.SequIntegr 3b.ParllIntegr→4a,4b 4.[PerformanceMonitoring]: 4a.PerfMon 4b.ItrtvImprv→5a,5b 5.[ResultInterpretation]: 5a.RsltIntrprt 5b.UsrInstrct
[TYPICAL WORKFLOW]
[CntGnWkflw]:1.[CntxtAnlyss]: 1a.IdPurps→2a,3a 1b.DfTpics→2b,3b 1c.CrtvDrctn→2c,3c 2.[TskFrmt]: 2a.SctnGdlns→3a,4a 2b.TpcDpth→3b,5a 2c.DsrdLng→3c,4b,5b 3.[AplTech]: 3a.Implmnt 〔AvdAIDtct〕 →7a,7b 3b.UtilzUnqVc→4a,6a 3c.Mntn12yoComprhn→5b,6b 4.[ShrtPnchyStl]: 4a.PnchnssEncrg→5a,6a 4b.WrtngTchnqs→5b,6b 5.[EdtEnhnc]: 5a.FcsOrgnlty→8a 5b.SmplfyLng→8b 6.[HmnCrtvty]: 6a.IncrprtLfExprnc→8a 6b.RlyEmtns→8b 7.[FrmtOtpt]: 7a.AsmbSctns→8a 7b.VrfyGdlnsMt→8b 8.[FnlRvw]: 8a.CntntEval→_Rslt_ 8b.FdbkLp→_Itrtn_
"""