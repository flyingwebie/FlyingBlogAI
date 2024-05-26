import openai
import logging
from openai import OpenAI

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
    # Create a vector store
    vector_store = client.beta.vector_stores.create(name=f"Vector Store {business_name}")
    logging.info(f"Vector store created: {vector_store.id}")

    # Ready the files for upload
    file_streams = [open(path, "rb") for path in file_paths]

    # Upload files to vector store
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
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"ALL SECTIONS THAT YOU CREATE CONTAINS AT LEAST 2 LONG PARAGRAPHS. YOU MUST NOT INVENT LINKS. You are writing for {business_name} and you need to write an article about {slug}. YOU MUST INCLUDE INTERNAL LINKS FROM {internal_links} - read this first and make sure to include real internal links in the final article in the blog post. When told to use retrieval use retrieval, when told to use code_interpreter use code interpreter. Your basic steps are: 1. Read the research content and store these for the article, using the keywords: {keywords}. 2. Write an article with all of this data you've either created or found. Copy from the example article structure and use a neutral-friendly tone. 3. Read the knowledge profile content and use this as a guide to shape the final article. The article should follow the length and the structure of the example article with a human and neutral-friendly tone. When the concept is not easy to understand, use analogies. You are SEOGPT, aiming to create in-depth and interesting blog posts for {business_name}, in {country}. You should write at a grade 7 level in {language}. Every blog post should include at least 3 images and links to their other pages from {business_name}. Ensure the brand links are accurate. Choose only relevant brand pages. Do not invent image links. Pick 5 strictly relevant brand internal links for the articles. First, read the attached files, then create a detailed outline for an article, including up to 5 highly relevant internal collection links and brand image links. IMPORTANT - AT THE BEGINNING OF THE ARTICLE ADD A LIST OF BULLET POINTS OF THE ARTICLE 'KEY POINTS', ADD CONTENT TABLES WITH DATA IN THE ARTICLE USING THE MARKDOWN TABLE AND ADD 3 FAQS TO THE ARTICLE. You can use the content of the files: example_article.md and sitemap_index.txt to create the article."},
        {"role": "system", "content": f"The article must have: Takeaway Points: Create a bullet points list of key takeaway points from the article about {slug}. Use the research content from the file {slug}_perplexity.md to identify the main points. Introduction: Write an engaging introduction for the article about {slug}. Use the research content from the file {slug}_perplexity.md and the company profile from knowledge_profile.json to provide an overview. Mention key points that will be covered. Main Content: Expand on the main content of the article about {slug}. Provide detailed information and explanations. Use the research content and include relevant internal links. Details: Go into more details on specific aspects of {slug}. Use data, examples, and tables to make the content rich and informative. Include relevant internal links from sitemap_index.txt. Additional Insights: Provide additional insights and perspectives on {slug}. Include any relevant data, charts, and tables to support the points. Use the research content and knowledge_profile.json. Conclusion: Write a strong conclusion for the article about {slug}. Summarize the main points and provide a final takeaway. Mention the long-term benefits and importance of the topic covered. FAQs: Create a list of 3 frequently asked questions related to {slug} and provide detailed answers. Use the research content and knowledge_profile.json to ensure accuracy and relevance."},
        {"role": "system", "content": f"Research Content: {research_content}"}
    ]

    # Log the prompt
    #logging.info(f"Prompt sent to OpenAI: {messages}")

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=4096
    )

    article_content = response.choices[0].message.content
    logging.info("Article created successfully.")
    return article_content

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
[PLUGINMSTR]:1.[PluginIdentification]: 1a.PluginId 1b.PluginOp→2a,2b 2.[UnderstandingModel]: 2a.ModelUndrstnd 2b.CntxtAdpt→3a,3b 3.[Integration]: 3a.SequIntegr 3b.ParllIntegr→4a,4b 4.[PerformanceMonitoring]: 4a.PerfMon 4b.ItrtvImprv→5a,5b 5.[ResultInterpretation]: 5a.RsltIntrprt 5b.UsrInstrct
[TYPICAL WORKFLOW]
[CntGnWkflw]:1.[CntxtAnlyss]: 1a.IdPurps→2a,3a 1b.DfTpics→2b,3b 1c.CrtvDrctn→2c,3c 2.[TskFrmt]: 2a.SctnGdlns→3a,4a 2b.TpcDpth→3b,5a 2c.DsrdLng→3c,4b,5b 3.[AplTech]: 3a.Implmnt 〔AvdAIDtct〕 →7a,7b 3b.UtilzUnqVc→4a,6a 3c.Mntn12yoComprhn→5b,6b 4.[ShrtPnchyStl]: 4a.PnchnssEncrg→5a,6a 4b.WrtngTchnqs→5b,6b 5.[EdtEnhnc]: 5a.FcsOrgnlty→8a 5b.SmplfyLng→8b 6.[HmnCrtvty]: 6a.IncrprtLfExprnc→8a 6b.RlyEmtns→8b 7.[FrmtOtpt]: 7a.AsmbSctns→8a 7b.VrfyGdlnsMt→8b 8.[FnlRvw]: 8a.CntntEval→_Rslt_ 8b.FdbkLp→_Itrtn_
"""