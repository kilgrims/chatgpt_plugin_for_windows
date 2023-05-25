import openai
import json
import os
import sys
import io

sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
#path = os.path.dirname("os.path.abspath(__file__)")
path = os.path.abspath(".")

def end_handle(p_t,c_t):
    f1=open(path+r"/config.json","r",encoding="utf-8")
    js=json.load(f1)
    f1.close()
    js["prompt_tokens"]=str(int(js["prompt_tokens"])+p_t)
    js["completion_tokens"]=str(int(js["completion_tokens"])+c_t)
    f2=open(path+r"/config.json","w",encoding="utf-8")
    json.dump(js,f2)
    f2.close()
    input("\n输入任意值结束程序\n")
    sys.exit()


f_js=open(path+"/config.json","r",encoding="utf-8")
js=json.load(f_js)
f_js.close()

openai.api_key=js["API_KEY"]

print("欢迎使用gpt\n")
op=input("输入1进入单句问答，输入2进入连续对话，输入3打印一条对话，输入4设置一条对话前提：")

if op=="3":
    file_name=input("输入文件名称（不用包括后缀名  .json  ，注意文件要放在conversation文件夹中）：\n")
    file_name=path+"/conversation/"+file_name+".json"
    try:
        conversation_file=open(file_name)
    except IOError:
        print("文件打开失败，可能不存在或者没有权限！")
        input("\n输入任意值结束程序\n")
        sys.exit()
    conver=(json.load(conversation_file))["message"]
    conversation_file.close()
    i=1
    for con in conver:
        msg="\n\n"+str(i)+"#:\nrole:"+str(con["role"])+"\ncontent:\n"+str(con["content"])
        print(msg)
        i=i+1
    input("\n输入任意值结束程序\n")
    sys.exit()


if op=="4":
    os.system("cls")
    file_name=input("输入前提文件文件名称（不用包括后缀名  .json  ，文件会自动保存在conversation文件夹中）：\n")
    file_name=path+"/conversation/"+file_name+".json"
    
    front_f=open(file_name,"w+",encoding="utf-8")
    role_name=""
    front_conver=[]
    while(role_name!="end"):
        role_name=input("\n输入角色，1代表用户，2代表系统，输入end结束程序：")
        if role_name=="end":
            break
        if role_name=="1":
            role="user"
        else:
            role="system"
        msg=input("\n输入你的预设话语：\n")
        front_conver.extend([{"role":role,"content":msg}])
    os.system("cls")
    js_save={"prompt_tokens":"0","completion_tokens":"0","message":front_conver}

    json.dump(js_save,front_f)
    front_f.close()

    print("输入结束，您的文件保存为:"+file_name+"\n")
    input("\n输入任意值结束程序\n")
    sys.exit()




if (op!='1')&(op!='2'):
    print("输入错误!")
    sys.exit()

os.system("cls")

op2=input("输入1加载对话或前提，输入2直接开始：")

prompt_tokens=0
completion_tokens=0

conver=[]

if (op2!="1")&(op2!="2"):
    print("输入错误!")
    sys.exit()

if op2=="1":
    file_name=input("输入文件名称（不用包括后缀名  .json  ，注意文件要放在conversation文件夹中）：\n")
    file_name=path+"/conversation/"+file_name+".json"
    try:
        conversation_file=open(file_name)
    except IOError:
        print("文件打开失败，可能不存在或者没有权限！")
        sys.exit()
    conver=(json.load(conversation_file))["message"]
    conversation_file.close()
else:
    conver=[]

os.system("cls")

if op=="1":
    msg=input("输入您的问题：\n")
    conver.extend([{"role":"user","content":msg}])
    ans=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=conver)
    print("\n\n回答：\n")
    print(ans.choices[0].message.content)
    

    prompt_tokens=int(ans.usage["prompt_tokens"])
    completion_tokens=int(ans.usage["completion_tokens"])
    end_handle(prompt_tokens,completion_tokens)
else:
    i=1
    while(i!=0):
        r="#"+str(i)+":输入您的问题：\n"
        msg=input(r)
        
        conver.extend([{"role":"user","content":msg}])
        ans=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=conver)
        print("\n\n回答：\n")
        print(ans.choices[0].message.content)

        conver.extend([{"role":"assistant","content":ans.choices[0].message.content}])

        prompt_tokens=int(ans.usage["prompt_tokens"])+prompt_tokens
        completion_tokens=int(ans.usage["completion_tokens"])+completion_tokens

        i=i+1

        en=input("\n\n是否结束（输入Y来结束）：")
        if en=="Y":
            en=input("\n是否保存（输入Y来保存）：")
            if en=="Y":
                file_save_name=input("输入保存文件名称：")
                file_save_name=path+"/conversation/"+file_save_name+".json"
                f_save=open(file_save_name,"w+",encoding="utf-8")
                js_save={"prompt_tokens":str(prompt_tokens),"completion_tokens":str(completion_tokens),"message":conver}
                json.dump(js_save,f_save)
                f_save.close()
        end_handle(prompt_tokens,completion_tokens)
