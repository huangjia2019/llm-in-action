from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser

# 提示模板
template = "创建含3个{text}元素的列表.\n\n{format_instructions}"
chat_prompt = ChatPromptTemplate.from_template(template)

# 输出解析器
output_parser = CommaSeparatedListOutputParser()
chat_prompt = chat_prompt.partial(format_instructions=output_parser.get_format_instructions())

# 模型
chat_model = ChatOpenAI(model="gpt-3.5-turbo")  

# 用LCEL组合
chain = chat_prompt | chat_model | output_parser

# 调用链
result = chain.invoke({"text": "国家"})
print(result)