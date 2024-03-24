import requests,json,os,time,functools,subprocess,zipfile
main_dir = os.path.join(os.getenv('TEMP'),'ligma balls') #imma change it to %temp% when i release this shit
if not os.path.exists(main_dir):os.mkdir(main_dir)
os.chdir(main_dir)
print(f'Working dir:{main_dir}')
try:openaikey = open('bin\\OpenAI key.txt', 'r').read()
except FileNotFoundError:#first run setuppppppp
    bin_dir = os.path.join(main_dir,'bin')
    try:os.mkdir(bin_dir)
    except:pass
    print("Đang tải xuống file,hãy đợi chút")
    from tqdm.auto import tqdm #for fancy download progress bar
    response = requests.get('http://localhost:8000/a.zip', stream=True)
    with tqdm.wrapattr(open(os.path.join(main_dir,'a.zip'), "wb"), "write", miniters=1,total=int(response.headers.get('content-length', 0)),desc='a.zip') as fout:
        for chunk in response.iter_content(chunk_size=4096):fout.write(chunk)
    fout.close()
    with zipfile.ZipFile('a.zip', 'r') as zip_ref:zip_ref.extractall('bin')
    os.remove('a.zip')
    open(os.path.join('bin','OpenAI key.txt'), 'w').write(input("Hãy nhập OpenAI API Key của bạn "))
openaikey = open(os.path.join('bin','OpenAI key.txt'),'r').read()
if not openaikey:open(os.path.join('bin','OpenAI key.txt'), 'w').write(input("Hãy nhập OpenAI API Key của bạn "))
from openai import OpenAI;client = OpenAI(api_key=openaikey)
client.api_key = openaikey


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):start_time = time.time();val = func(*args, **kwargs);end_time = time.time();run_time = end_time - start_time;print(f"Execute {func.__name__}() took {run_time:.4f}s.");return val
    return wrapper


# @timer
# def ___():
#     version = "8.0\n"#there is a newline on my stupid github page and i dont want to use .replace()
#     newestver = requests.get("https://raw.githubusercontent.com/itsnd64/IOE-Cheat/main/version.txt").text
#     if version != newestver:print("Đã có bản hack mới")
# ___()

input = json.loads(input("smthing idk?"))
headers = {"Content-type": "application/json", "Accept": "text/plain","Accept-Encoding": "gzip, deflate"}
os.system("cls")
def p(string :str):os.sys.stdout.write(str(string) + '\n')#just for fun

try:input["api_key"]
except KeyError:#handle getinfo
    print("Got getinfo")
    token = input["data"]["token"]
    examKey = input["data"]["game"]["examKey"]
    api_key = ""
    r = input
else:#handle startgame
    print("Got startgame")
    token = input["token"]
    api_key = input["api_key"]
    examKey = input["examKey"]
    r = json.loads(requests.post("https://api-edu.go.vn/ioe-service/v2/game/getinfo",headers=headers,data=json.dumps({"IPClient": "","deviceId": "","api_key": api_key,"token": token}),).text)

try:
    questions = r["data"]["game"]["question"]
    quesnum = len(questions)
    os.system("cls")
except TypeError:
    print("Token ko hợp lệ")
    exit()


def run_once(func):#idk what is this but it should work
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            func(*args, **kwargs)
            wrapper.has_run = True
    wrapper.has_run = False
    return wrapper
def checkans(ans :str = "",qid :str = "",point :int = 10,isfinishgame :bool = False,fans :str = ""):
    """Finishgame syntax:{"ans": ans,"qid": qid,"point": 10/20/etc},..."""
    if isfinishgame:
        finishgamejson = {
            "api_key": api_key,
            "token": token,
            "serviceCode": "IOE",
            "examKey": examKey,
            "ans": json.loads(f'[{fans}]')
        }
        print(finishgamejson)
        r3 = json.loads(requests.post(
        "https://api-edu.go.vn/ioe-service/v2/game/finishgame",
        json=finishgamejson,
    ).text)
        print(r3)
        if r3["IsSuccessed"]:
            print(f'Điểm: {r3["data"]["totalPoint"]}\nThời gian: {r3["data"]["time"]}s')
        else:
            print(r3)
    else:
        jsonans = {
        "IPClient": "",
        "deviceId": "",
        "serviceCode": "IOE",
        "api_key": api_key,
        "token": token,
        "examKey": examKey,
        "ans": {"questId": qid, "point": point, "ans": ans},
    }
        r2 = requests.post(
            "https://api-edu.go.vn/ioe-service/v2/game/answercheck",
            headers=headers,
            data=json.dumps(jsonans),
        )
#        print(r2.text)
        return json.loads(r2.text)["data"]["point"] == 10

def sendmsg(prompt):
    print(prompt)
    completion = client.completions.create(model="gpt-3.5-turbo-instruct",prompt=prompt,max_tokens=600,temperature=0)
    return completion.choices[0].text

def jsonStrHandler(astr):return astr if astr and astr[0] == '"' and astr[-1] == '"' else astr.replace('"', '\\"') if '"' in astr else f'"{astr}"'

@run_once
@timer
def autobaibth():
    fans = ""
    for i2 in range(quesnum):
        print("Tìm đáp án câu" + " " + str(i2+1))
        qid = r["data"]["game"]["question"][i2]["id"]
        answers = r["data"]["game"]["question"][i2]["ans"]
        for i in range(len(answers)):
            ans = answers[i]["content"]
            if checkans(ans,qid,10):
                fans += f'{{"ans": {jsonStrHandler(ans)},"questId": "{qid}","point": 10}},'
                print(jsonStrHandler(ans))
                break
    print("Gửi chuỗi json tạo được")
    print(fans[:-1])
    checkans(isfinishgame=True,fans=fans[:-1])
def autobaitf():
    fans = ""
    for i2 in range(quesnum):
        qid = r["data"]["game"]["question"][i2]["id"]
        answers = [{"content": "True"}, {"content": "False"}]
        for i in range(2):
            ans = answers[i]["content"]
            if checkans(ans,qid,10):
                fans += f'{{"ans": {jsonStrHandler(ans)},"questId": "{qid}","point": 10}},'
                break
    print(fans[:-1])
    checkans(isfinishgame=True,fans=fans[:-1])

@run_once
def baichontu(isTF :bool = False):
    for i2 in range(quesnum):
        qid = r["data"]["game"]["question"][i2]["id"]
        if isTF:answers = [{"content": "True"}, {"content": "False"}]
        else:answers = r["data"]["game"]["question"][i2]["ans"]
        for i in range(len(answers)):
            ans = answers[int(i)]["content"]
            if checkans(ans,qid,10):
                print(str(i2 + 1) + "." + ans)
                break


def sortcri(list):return list["orderTrue"]
@run_once
def baisapxep():
    quesnum = 10 #mac dinh :>        uh idk why did i write this
    for i2 in range(quesnum):
        answers = r["data"]["game"]["question"][i2]["ans"]
        answers.sort(key=sortcri)
        ans = ""
        for i3 in range(len(answers)):
            ans += answers[i3]["content"] + " "
        print(str(i2+1)+"."+ans)

#base64_decode_this_to_get_useless_ai_based_solver = 'IyBkZWYgQmFpRHVuZ0FJKHR5cGUpOgojICAgICBwcmludCgiTMawdSDDvTogQsOgaSDEkcaw4bujYyBsw6BtIGLhu59pIEFJKENoYXRHUFQpIG7Dqm4gc2FpIHPDs3Qga2jDtG5nIHRo4buDIHRyw6FuaCBraOG7j2kiKQojICAgICB3YXQgPSByWyJkYXRhIl1bImdhbWUiXVsiU3ViamVjdCJdWyJjb250ZW50Il0KIyAgICAgc2VuZG1zZyhmJ3sixJDhu41jIGLDoGkgdsSDbiBzYXUifVxue3dhdH0nKQojICAgICBxdWVzdGlvbnMgPSAiIgojICAgICBmb3IgaTIgaW4gcmFuZ2UobGVuKHJbImRhdGEiXVsiZ2FtZSJdWyJxdWVzdGlvbiJdKSk6CiMgICAgICAgICBxaWQgPSByWyJkYXRhIl1bImdhbWUiXVsicXVlc3Rpb24iXVtpMl1bImlkIl0KIyAgICAgICAgIHF1ZXN0aW9uID0gclsiZGF0YSJdWyJnYW1lIl1bInF1ZXN0aW9uIl1baTJdWyJjb250ZW50Il1bImNvbnRlbnQiXQojICAgICAgICAgcXVlc3Rpb25zID0gZid7cXVlc3Rpb25zfVxueyJDw6J1In0ge2kyKzF9OntxdWVzdGlvbn0nCiMgICAgIG1hdGNoIHR5cGU6CiMgICAgICAgICBjYXNlICJkaWVudHUiOgojICAgICAgICAgICAgIHByaW50KHNlbmRtc2coZid7IsSQaeG7gW4gdOG7qyBk4buxYSB0aGVvIHPhu5EgbMaw4bujbmcgZOG6pXUgaG9hIHRo4buLIn1cbiJ7cXVlc3Rpb25zfSInKSkKIyAgICAgICAgIGNhc2UgInRmIjoKIyAgICAgICAgICAgICBwcmludChzZW5kbXNnKGYneyJU4burIMSRb+G6oW4gdsSDbiB0csOqbiB0cuG6oyBs4budaSBjw6J1IGjhu49pIFRydWUgRmFsc2Ugc2F1OiJ9XG57cXVlc3Rpb25zfScpKQojICAgICAgICAgY2FzZSAiY29ubG9uIjoKIyAgICAgICAgICAgICBxdWVzdGlvbnMgPSAiIgojICAgICAgICAgICAgIGZvciBpMiBpbiByYW5nZShsZW4oclsiZGF0YSJdWyJnYW1lIl1bInF1ZXN0aW9uIl0pKToKIyAgICAgICAgICAgICAgICAgcWlkID0gclsiZGF0YSJdWyJnYW1lIl1bInF1ZXN0aW9uIl1baTJdWyJpZCJdCiMgICAgICAgICAgICAgICAgIHF1ZXN0aW9ucyA9IHJbImRhdGEiXVsiZ2FtZSJdWyJxdWVzdGlvbiJdW2kyXVsiY29udGVudCJdWyJjb250ZW50Il0KIyAgICAgICAgICAgICBwcmludChzZW5kbXNnKGYneyLEkOG7jWMgYsOgaSB2xINuIHNhdSJ9XG57d2F0fVxueyLEkGnhu4FuIGPDoWMgdOG7qyBzYXUgdsOgbyDEkW/huqFuIHbEg246In1cbntxdWVzdGlvbnN9JykpCiMgICAgICAgICBjYXNlIF86CiMgICAgICAgICAgICAgcmFpc2UgVHlwZUVycm9yKCJ0eXBlIGNo4buJIGPDsyB0aOG6vyBi4bqxbmcgZGllbnR1LHRmLGNvbmxvbiIp'

#functions for listening test
#TODO: organize this shit
temp_dir = os.path.join("bin","temp")
output_file = os.path.join(temp_dir,"output.mp3")
def temp_init():
    if not os.path.exists(temp_dir):os.makedirs(temp_dir);print(f'Đã tạo: {temp_dir}')
    else:print(f'dir alr exist')
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)
            print(f'Deleted {file_path}')
def dlaudio(url, save_path):
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as audio_file:
        for chunk in response.iter_content(chunk_size=1024):
            audio_file.write(chunk)
def readaudio(filepath):
    audio_file= open(filepath, "rb")
    return client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="text"
    )[:-1]
def combinemp3s():
    #warn:next line is huge and stupid bc for some reason my previous beautifully code sometime dont work with ffmpeg
    subprocess.run(['bin\\ffmpeg', '-i', 'bin\\temp\\0.mp3', '-i', 'bin\\lol.mp3', '-i', 'bin\\temp\\1.mp3', '-i', 'bin\\lol.mp3', '-i', 'bin\\temp\\2.mp3', '-i', 'bin\\lol.mp3', '-i', 'bin\\temp\\3.mp3', '-i', 'bin\\lol.mp3', '-i', 'bin\\temp\\4.mp3', '-i', 'bin\\lol.mp3', '-i', 'bin\\temp\\5.mp3', '-i', 'bin\\lol.mp3', '-i', 'bin\\temp\\6.mp3', '-i', 'bin\\lol.mp3', '-i', 'bin\\temp\\7.mp3', '-i', 'bin\\lol.mp3', '-i', 'bin\\temp\\8.mp3', '-i', 'bin\\lol.mp3', '-i', 'bin\\temp\\9.mp3', '-i', 'bin\\lol.mp3', '-filter_complex', '[0:a][1:a][2:a][3:a][4:a][5:a][6:a][7:a][8:a][9:a][10:a][11:a][12:a][13:a][14:a][15:a][16:a][17:a][18:a][19:a]concat=n=20:v=0:a=1[aout]', '-map', '[aout]', 'bin\\temp\\output.mp3'], check=True)
def stupiddiff(a, b):#i should've use set() but it works anyway
    diff = ''
    for a,b in zip(a,b):
        if a != b:diff += a
    return diff
@timer
def autobaiheo():#ioe_game_16
    print("Lưu ý:Bài được làm bởi AI(ChatGPT) nên sai sót không thể tránh khỏi")
    answers = ''
    ques = r["data"]["game"]["Subject"]["content"]
    qid = r["data"]["game"]["question"][0]["id"]
    for i in r["data"]["game"]["question"][0]["ans"]:answers += i["content"] + ","
    ans = sendmsg(f'{"Đọc bài văn sau"}\n{ques}\n{'Điền các từ sau vào đoạn văn cách nhau bởi dấu | chỉ cần câu trả lời'}\n{answers[:-1]}')[1:]
    fans = '|'.join([line.split('. ')[1] for line in ans.split('\n') if line])
    fans = f'{{"questId": {qid},"ans": "{fans}","Point": 100}}'
    checkans("","",0,True,fans)
@timer
def autobainghe():
    temp_init()
    print("Lưu ý:Bài được làm bởi AI(Whisper) nên sai sót không thể tránh khỏi")
    qids = []
    questions = []
    for i in range(quesnum):
        qids.append(r["data"]["game"]["question"][i]["id"])
        questions.append(r["data"]["game"]["question"][i]["content"]["content"])
        dlaudio(r["data"]["game"]["question"][i]["Description"]["content"],temp_dir +"\\"+str(i)+".mp3")
        print(f'Trạng Thái: Tải xuống bài nghe {i+1}')
    print(f'Trạng Thái: Kết hợp các file mp3')
    combinemp3s()
    result_list = [a for a in readaudio(output_file).split(" Gay. ")[:-1] if a]
    idk = []
    for a,b in zip(result_list,questions):idk.append(stupiddiff(a,b).replace('.',''))
    flist = [{"qid": qid, "ans": answer, 'point': 10} for qid, answer in zip(qids, idk)]
    fans = ""
    for item in flist:fans += f'{{"qid": {item["qid"]}, "ans": "{item["ans"]}", "point": {item["point"]}}},'
    p(fans[:-1])
    checkans(isfinishgame=True,fans=fans[:-1])
#TODO: add output to autobaitf()
match r["data"]["gameDesc"]:
    case "The coral reefs have been destroyed; the dolphin Hubert and his friends in the ocean have left. You are the diver whose mission is to recreate such reefs and bring marine creatures back.\r\nListen carefully and decide whether the given statement is true or false by choosing the relevant button. You can replay the recording if necessary. You have 20 minutes to answer all the questions. \r\nYou will get points for each correct answer and deserved results with each score range you achieve.\r\nCheck your score and completion time at the end of the test. \r\nThe test is over when you submit all your answers or the time is up.":
        autobaitf()
    case "IOE's jewels are lost at sea! Accompany with Dai the octopus to collect them all by putting the words in the right order to make meaningful sentences. The words will go in the order of the clicks. \r\nDo as many times as you like until you satisfy and click ANSWER to confirm your final decision. You have 20 minutes to answer all the questions. \r\nRemember that the hints will turn into foam if you cannot give a correct answer. You will get points for each correct answer and deserved results with each score range you achieve.\r\nCheck your score and completion time at the end of the test.\r\nThe test is over when you submit all your answers or the time is up. ":
        pass#bai sap xep