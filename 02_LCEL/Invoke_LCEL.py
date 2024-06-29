# 导入所需的库
from dotenv import load_dotenv  # 用于加载环境变量
load_dotenv()  # 加载 .env 文件中的环境变量

from langchain_core.runnables import RunnablePassthrough
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("告诉我关于{flower}的故事")
output_parser = StrOutputParser()
model = ChatOpenAI(model="gpt-3.5-turbo")

# 用LCEL构造链
chain = (
    {"flower": RunnablePassthrough()} 
    | prompt # 提示
    | model # 模型
    | output_parser # 输出解析
)

# 执行链
result = chain.invoke("玫瑰")
print(result)