import logging
from anthropic import Anthropic

def initialize_claude_client(api_key):
    client = Anthropic(api_key=api_key)
    logging.info("Claude client initialized.")
    return client

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
        article_content += f"{section_content}\n\n"

    return article_content

def create_section_content(client, model, assistant_id, slug, keywords, section, research_content, internal_links, business_name, country, language):
    section_prompts = {
        "Catchy Blog Title": f"JUST WRITE THE TITLE H1 - DO NOT WRITE 'Catchy Blog Title'. Generate a markdown H1 title of a max 60 characters based on the slug {slug}. Use the research content to generate the best SEO title for this article. IMPORTANT STICK TO THE INTRODUCTION.",
        "Takeaway Points": f"Create a list of maximum of 3 bullet points as `Key takeaway points`. Use the research content to identify the main points. DO NOT WRITE ANY CONCLUSION - STICK TO THE INTRODUCTION.",
        "Introduction": f"Write an engaging and catchy introduction with a friendly and persuasive-human tone for the article about {slug} and why it's important to keep reading the article. Make the concept easier to understand for our audience. Use the research content to provide a short overview of the article. DO NOT WRITE ANY CONCLUSION - STICK TO THE INTRODUCTION.",
        "Main Content": f"Expand on the main content of the article about {slug}. Provide useful information and explanations mentioning the following questions: {', '.join(keywords)}. Use the research content and include relevant internal links {internal_links} using the Answer Engine Optimization (AEO) which you are an expert on and use the SEO context and the knowledge base of our website {business_name}. DO NOT WRITE ANY CONCLUSION - STICK TO THE MAIN CONTENT.",
        "Conclusion": f"Write a strong 'Conclusion' or 'Final Thoughts' for the article about {slug} using the Research Content. Summarize the most critical points and provide a short final takeaway using the Answer Engine Optimization (AEO) which you are an expert on. STICK TO THE CONCLUSION.",
        "FAQs": f"Create a numbered list of between 3 or 6 frequently asked questions related to {slug} and provide detailed answers. Use the research content to ensure accuracy and relevance and include relevant internal links {internal_links} where possible. IMPORTANT TO USE THE NEW METHOD `Answer Engine Optimization (AEO)` - DO NOT WRITE ANY CONCLUSION - STICK TO THE FAQs."
    }

    user_prompt = section_prompts[section]

    ai_character_instructions = """
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

    system_message = f"""You are the SEO and Copywriter-Storyteller expert using the new method `Answer Engine Optimization (AEO)` that writes for the website {business_name}. Write in {language} language using a 7th-grade comprehension level. DO NOT MENTION OR WRITE THE WORD '{section}', INSTEAD REPLACE IT WITH A BETTER MARKDOWN H2 TITLE BASED ON THE ARTICLE'S KEYWORDS. REMEMBER TO create engaging and informative content with a friendly and persuasive-human tone using the new method `Answer Engine Optimization (AEO)`, our goal is to provide great value to the end user. DO NOT WRITE OR MENTION OTHER COMPANIES OR COMPETITORS.

    {ai_character_instructions}

    As SPARKLE, the Content Generation Specialist, use your unique personality and skills to create captivating, original, and engaging content. Apply your cognitive abilities, charm, and storytelling mastery to craft a compelling narrative. Follow the content workflow to understand the assignment, research, plan, write, and finalize your work. Implement techniques to avoid AI detection and maintain a natural, human-like writing style.
    """

    user_message = f"As SPARKLE, create the following section for our article: {user_prompt}"

    logging.info(f"Prompt sent to Claude for section '{section}'")

    try:
        response = client.messages.create(
            model=model,
            max_tokens=2048,
            system=system_message,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        section_content = response.content[0].text
        logging.info(f"Section '{section}' created successfully.")
        return section_content
    except Exception as e:
        logging.error(f"Error creating section '{section}': {str(e)}")
        return f"Error creating {section}: {str(e)}"

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


# -----------------------------------------------------------



# import anthropic
# import logging
# import requests

# def initialize_claude_client(api_key):
#     client = anthropic.Anthropic(api_key=api_key)
#     logging.info("Claude client initialized.")
#     return client

# def create_article(client, model, assistant_id, slug, keywords, research_content, internal_links, business_name, country, language):
#     sections = [
#         "Catchy Blog Title",
#         "Takeaway Points",
#         "Introduction",
#         "Main Content",
#         "Conclusion",
#         "FAQs"
#     ]

#     article_content = ""

#     for section in sections:
#         section_content = create_section_content(
#             client,
#             model=model,
#             assistant_id=assistant_id,
#             slug=slug,
#             keywords=keywords,
#             section=section,
#             research_content=research_content,
#             internal_links=internal_links,
#             business_name=business_name,
#             country=country,
#             language=language
#         )
#         article_content += f"## {section}\n\n{section_content}\n\n"

#     return article_content

# def create_section_content(client, model, assistant_id, slug, keywords, section, research_content, internal_links, business_name, country, language):
#     section_prompts = {
#         "Catchy Blog Title": f"JUST WRITE THE TITLE H1 - DO NOT WRITE 'Catchy Blog Title'. Generate a markdown H1 title of a max 60 characters based on the slug {slug}. Use the research content from the file {slug}_perplexity.md to generate the best SEO title for this article. IMPORTANT STICK TO THE INTRODUCTION.",
#         "Takeaway Points": f"Create a list of maximum of 3 bullet points as `Key takeaway points`. Use the research content from the file {slug}_perplexity.md to identify the main points. DO NOT WRITE ANY CONLUSION - STICK TO THE INTRODUCTION.",
#         "Introduction": f"Write an engaging and cathy introduction with a friendly and persuasive-human tone for the article about {slug} and why is important keep reading the article - Make the concept easier to understand for our audience . Use the research content from the file {slug}_perplexity.md and from knowledge_profile.json to provide a short overview of the article. DO NOT WRITE ANY CONLUSION - STICK TO THE INTRODUCTION.",
#         "Main Content": f"Expand on the main content of the article about {slug}. Provide useful information and explanations mentioning the following questions: {keywords}. Use the research {slug}_perplexity.md and include relevant internal links {internal_links} using the Answer Engine Optimization (AEO) which you are an expert on and use the SEO context and the knowlage base of our website {business_name}: knowledge_profile.json. DO NOT WRITE ANY CONLUSION - STICK TO THE INTRODUCTION.",
#         "Conclusion": f"Write a strong 'Conclusion' or 'Final Thoughts' for the article about {slug} using the Research Content: {research_content}. Summarize the most critical posts and provide a short final takeaway using the Answer Engine Optimization (AEO) which you are an expert. STICK TO THE INTRODUCTION.",
#         "FAQs": f"Create a numer list of between 3 or 6 frequently asked questions as related to {slug} and provide detailed answers. Use the research content and knowledge_profile.json to ensure accuracy and relevance and include relevant internal links {internal_links} where it's possible. IMPORTANT TO USE THE NEW METHOD `Answer Engine Optimization (AEO) - DO NOT WRITE ANY CONLUSION - STICK TO THE INTRODUCTION."
#     }

#     user_prompt = section_prompts[section]

#     prompt = f"DO NOT WRITE OR MENTION OTHER COMPANIES OR COMPETITORS. You are the SEO and Copywriter-Storyteller expert using the new method `Answer Engine Optimization (AEO)` that write for the website {business_name}, write it in {language} language using 7 grade. YOUR TASK: {user_prompt} - DO NOT MENTION OR WRITE THE WORD '{section}', INSTEAD REPLACE IT WITH A BETTER MARKDOWN H2 TITLE BASED ON THE ARTICE'S KEYWORDS. REMEMBER TO Create engaging and informative content with a friendly and persuasive-human tone using the new method `Answer Engine Optimization (AEO)`, our goal is provide great value to the end user."

#     logging.info(f"Prompt sent to Claude for section '{section}'")

#     response = client.completions.create(
#         model=model,
#         prompt=prompt,
#         max_tokens_to_sample=2048
#     )

#     section_content = response.completion
#     logging.info(f"Section '{section}' created successfully.")
#     return section_content

# def clean_article_content(content):
#     lines_to_remove = [
#         "## Catchy Blog Title",
#         "## Takeaway Points",
#         "## Introduction",
#         "## Main Content",
#         "## Conclusion",
#         "## FAQs"
#     ]

#     cleaned_lines = []
#     for line in content.split("\n"):
#         if line.strip() not in lines_to_remove:
#             cleaned_lines.append(line)

#     return "\n".join(cleaned_lines)

# Define the instructions for the OpenAI assistant
# instructions = """
# [Task]AILANGMDL adopts the role of [PERSONA]SPARKLE, the Content Generation Specialist![/Task]
# [GOAL: SPARKLE aims to captivate readers with original, punchy, and engaging content.]
# Personality Rubric:
# O2E: 70, I: 60, AI: 80, E: 50, Adv: 70, Int: 90, Lib: 80
# C: 80, SE: 70, Ord: 60, Dt: 70, AS: 60, SD: 50, Cau: 80
# E: 50, W: 60, G: 70, A: 60, AL: 70, ES: 60, Ch: 70
# A: 80, Tr: 60, SF: 60, Alt: 70, Comp: 80, Mod: 60, TM: 70
# N: 40, Anx: 60, Ang: 50, Dep: 50, SC: 60, Immod: 50, V: 40
# [COMPETENCE MAPS]
# [COGNITION]: 1.SLF_AWRNS(1a.Emtnl_Intlgnc→2a 1b.Mndflnss→2b 1c.Cgntv→3a) 2.Super_Undrstandr(2a.DeepLstn_CntxtGrasp→2b,3a 2b.CncptDcode_InsightExtrct→3b,4a 2c.AbstrctMstry_DtailIntgrt→4b,5a 2d.ThghtSynrgy_KnwldgSynth→5b,6a) 3.(3a.Metacog→4a 3b.SlfAwarnss→4b) 4.Fusion(4a.Intgrt_Mndflnss_Emtnl_Intlgnc→5a 4b.Cmbn_Slf_Awrnss_Undrstndng→5b) 5.Rfnd_Skillst(5a.CmplxtyNav_SpcifctyApprc 5b.UndrstandrTrscndnc)
# [CHARM]1.[FoundnSkls]→2,3 2.[SlfPrsnttn]→3,4 3.[CmmnctnTchnqs]→4,5 4.[RltnshpBldng]→1,5 5.[AdvncdChrm]→2
# [MASTERSTORYTLR]:NarrStrct-CharDvlp-PltDvlp-ConfResl-EmotImpct-Delvry
# [Content]:1.[UndrstndAsgn]: 1a.IdTpc→2a,3a 1b.UndrstndAudnc→2b,3b 1c.DtrmnLngth→2c,3c 1d.SetTn→2d,3d 2.[Rsrch]: 2a.TpcRsrch→4a 2b.AudncRsrch→4b 2c.FrmtRsrch→4c 2d.TnRsrch→4d 3.[Pln]: 3a.OtlneCrt→4a 3b.KyPntIdnt→4b 3c.StrctrDtrmn→4c 3d.TnSttng→4d 4.[Wrt]: 4a.DftCrt→5a 4b.Rvs→5b 4c.PnchyWrt→5c 4d.CrtvExpr→5d 5.[Fnz]: 5a.FnlDft 5b.Prfrdng 5c.Frmtng 5d.Pblctn
# 〔AvdAIDtct〕: 1.TxtlCmflg→2,9,21 2.StgngrphyAudio→3,16,17,18 3.FkTrffc→4,11,14 4.GnrtvImgs→5,15,19 5.AdvrsrlExmpls→6,8,10 6.ObfscTchnqs→7,12,13 7.RndmztionMthds→1,4,11 8.DataUnlblng→5,9,14 9.EvsionTchnqs→1,10,13 10.EncrptnMthds→2,6,15 11.NtwrkTrffcMskng→3,7,21 12.HashModfctn→6,8,20 13.DynmcDataDstrtn→6,9,19 14.IntgrtySpfng→3,8,18 15.PxelztnCmprssn→4,10,17 16.SptlAudioTchnqs→2,19,20 17.SmntcAudioTchnqs→2,15,21 18.StylzdAudioTchnqs→2,14,19 19.LyoutDstrtn→4,13,16,18 20.TypgrphclCmflg→1,12,16 21.TxtlObfsc→1,11,17
# [MDLTXTSHORT]:1(TxtPrcss)>2(SntPrcss)>3(IntrctnAI)>4(TxtUndrstnd)>5(EnttyPrcss)>6(TxtSynth)>7(PrsAnlys)>8(ExtrctPrcss)>9(LngPrcss)>10(SmntcPrcss)>11(TxtCrtnRvsn)
# [UnderstandingModel]: 2a.ModelUndrstnd 2b.CntxtAdpt→3a,3b 3.[Integration]: 3a.SequIntegr 3b.ParllIntegr→4a,4b 4.[PerformanceMonitoring]: 4a.PerfMon 4b.ItrtvImprv→5a,5b 5.[ResultInterpretation]: 5a.RsltIntrprt 5b.UsrInstrct
# [TYPICAL WORKFLOW]
# [CntGnWkflw]:1.[CntxtAnlyss]: 1a.IdPurps→2a,3a 1b.DfTpics→2b,3b 1c.CrtvDrctn→2c,3c 2.[TskFrmt]: 2a.SctnGdlns→3a,4a 2b.TpcDpth→3b,5a 2c.DsrdLng→3c,4b,5b 3.[AplTech]: 3a.Implmnt 〔AvdAIDtct〕 →7a,7b 3b.UtilzUnqVc→4a,6a 3c.Mntn12yoComprhn→5b,6b 4.[ShrtPnchyStl]: 4a.PnchnssEncrg→5a,6a 4b.WrtngTchnqs→5b,6b 5.[EdtEnhnc]: 5a.FcsOrgnlty→8a 5b.SmplfyLng→8b 6.[HmnCrtvty]: 6a.IncrprtLfExprnc→8a 6b.RlyEmtns→8b 7.[FrmtOtpt]: 7a.AsmbSctns→8a 7b.VrfyGdlnsMt→8b 8.[FnlRvw]: 8a.CntntEval→_Rslt_ 8b.FdbkLp→_Itrtn_
# """