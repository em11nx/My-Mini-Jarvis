from openai import OpenAI
import speech_recognition
import string

isRunning = True

user_selection = input("What mode would you like:\nTalk and get text responce: T\nType and get text responce: W\n>")

UserVoiceRecognizer = speech_recognition.Recognizer()

client = OpenAI (
    api_key=''
)

#based off https://techchannel.com/python/speech-to-text-conversion-using-python/ listens for audio and uses ai to convert it to text with no puncuation
def check_for_audio():
    try:
        #found audio
        with speech_recognition.Microphone() as UserVoiceInputSource:
 
            UserVoiceRecognizer.adjust_for_ambient_noise(UserVoiceInputSource, duration=0.5)

            print("Start talking")

            UserVoiceInput = UserVoiceRecognizer.listen(UserVoiceInputSource)

            with open("temp_audio.wav", "wb") as temp_audio_file:
                temp_audio_file.write(UserVoiceInput.get_wav_data())

            audio_file = open("temp_audio.wav", "rb")

            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
 
            UserVoiceInput_converted_to_Text = transcript.text.lower()

            No_Punc_UserVoiceInput_converted_to_Text = UserVoiceInput_converted_to_Text.translate(str.maketrans('', '', string.punctuation))

            print("Transcript Done")
            audio_gpt_perp_and_send(No_Punc_UserVoiceInput_converted_to_Text)
    
    #keyboard inputed something
    except KeyboardInterrupt:
        exit(0)
    
    #unknown audio
    except speech_recognition.UnknownValueError:
        pass

def audio_gpt_perp_and_send():
    audio_in = check_for_audio()
    prompt = audio_to_selective_prompt(audio_in, "jeff")
    if(prompt[0] == True):
        print("Sending to GPT")
        conntact_AI_Question(prompt[1])

def text_gpt_perp_and_send():
    prompt = input("Prompt: ")
    print("Sending to GPT")
    conntact_AI_Question("Jeff " + prompt)

#takes a string and converts it a list of words
def convert_str_to_words(string):
    string.replace(',', '')
    li = list(string.split(" "))
    return li

#takes a list of words and converts it to a string
def convert_words_to_str(words):
    li = " "
    return (li.join(words))

#checks a list of words for a word and returns a bool if it is in the list and with all words after the word
def check_for_word(list_of_words, looking_for):
    #print(list_of_words)
    command_words = []
    try:
        index = list_of_words.index(looking_for)
        for words in range(len(list_of_words) - index):
            command_words.append(list_of_words[index + words])
        print("Found Jeff")
        return [True, command_words]
    except ValueError:
        print("Failed to find Jeff")
        return [False, ""]

#takes a prompt and prints the responce from gpt-3.5-turbo
def conntact_AI_Question(prompt):
    if prompt == "jeff goodbye" or prompt == "jeff exit" or prompt == "jeff terminate" or prompt == "jeff end":
        exit(0)
    else:
        system_data = [
        {"role": "system", "content": "You are an assistant who's name is Jeff that helps with coding questions."},
        {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model= 'gpt-3.5-turbo',
            messages= system_data
        )
        oai_response = response.choices[0].message.content
        print("Assistant: " + oai_response)
        system_data.append({"role": "assistant", "content": oai_response})

#takes a string and activation word to take from then on to  
def audio_to_selective_prompt(text, activation_word):
    command_word_list = check_for_word(convert_str_to_words(text), activation_word)
    if(command_word_list[0] == False): return [False, ""]
    else: return [True, convert_words_to_str(command_word_list[1])]



while isRunning:
    if(user_selection.lower() == 't'):
        audio_gpt_perp_and_send()
    elif(user_selection.lower() == 'w'):
        text_gpt_perp_and_send()
    else:
        print("This: " + user_selection + " is not a vaild command.")
        user_selection = input("Please try again: ")