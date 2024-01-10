import SparkApi
from SparkApi import on_message_not_stream
appid = "######"
api_secret = "##########"
api_key ="####################"
domain = "generalv3"
Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"

text =[]

def getText(role,content):
    """
    官方实例
    :param role:
    :param content:
    :return:
    """
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getText_pro(role,content):
    """
    作者自己测试加入历史对话对数据处理的影响函数，效果还不错
    """
    jsoncon = {}
    one_put = """['货物/纸、纸制品及印刷品/纸及纸制品/手工制纸及纸板','货物/设备/车辆/摩托车/三轮摩托车/',]\n请从上面选项中选择一个属于下面文本的分类\n左侧边坡宣传标语   
        ,结果只输出1,2 ,如果都不属于输出0
    """
    text.append({'role':'user','content':one_put})
    text.append({'role': 'assistant', 'content': '0'})
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text


def spark_api(question):
    """
    作者自己写的函数，作用是直接返回最终结果，用于非流式问答
    :param question:
    :return:
    """

    question = checklen(getText("user",question))
    # print('question--->',question)

    SparkApi.answer = ""
    SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question,on_message_not_stream)
    text.clear()
    return SparkApi.answer


if __name__ == '__main__':

    # print(spark_api('讲个笑话'))  # 非流式输出
    # exit()
    while(1):  # 流式输出案例
        Input = input("\n" +"我:")
        question = checklen(getText("user",Input))
        SparkApi.answer =""
        print("星火:",end = "")
        SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
        res = getText("assistant",SparkApi.answer)
        # text.clear()
        # print(SparkApi.answer)


