from openai import OpenAI
import re

# Set your API key
def extract_waypoints(text):
    # pattern of 3 list values
    # pattern = r"\[\s*(\[\s*-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?\s*\](?:,\s*\[\s*-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?\s*\])*)\s*\]"
    # match = re.search(pattern, text, re.DOTALL)
    # if match:
    #     extracted_list = match.group(1)  # Extract the list content inside the outer brackets
    #     clean_string = "[" + extracted_list.replace(" ", "").replace("\n", "") + "]"
    #     return clean_string
    # else:
    #     return None

    # pattern of 4 list values
    pattern = r"\[\s*(\[\s*-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?\s*\](?:,\s*\[\s*-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?\s*\])*)\s*\]"

    match = re.search(pattern, text, re.DOTALL)
    if match:
        extracted_list = match.group(1)  # Extract list content
        clean_string = "[" + extracted_list.replace(" ", "").replace("\n", "") + "]"
        return clean_string  
    else:
        return None

def queryGPT_waypoints(timestamps):
    api_key = "sk-BmKxDbClXUMnzJCMo12rLA"
    client = OpenAI(api_key=api_key,
                    base_url="https://cmu.litellm.ai")
    # Define the prompt
    prompt = f"""You are choreographing a dance for a robot mounted to a table. You will help me generate the waypoints of this dance. 
    The allowable workspace for the robot is within the bounds of a 3-D rectangle. 
    The x,y,z coordinates of this bounded rectangle are: 
    \n\n[[0.35,-0.2,0.2], [0.35,0.2,0.2], [0.35,-0.2,0.6], [0.35,0.2,0.6], [0.7,-0.2,0.2], [0.7,0.2,0.2], [0.7,-0.2,0.6], [0.7,0.2,0.6]]
    \n Your response should also follow the format of the workspace bounds, which is a list of lists. 
    \n\nIn addition, we have a list of timestamps in seconds at which the movements should occur: 
    \n\n {timestamps}
    \n\n Respond with a plan of [x,y,z,t] waypoints for the dance in a list of arrays, with each waypoint corresponding to a timestamp 't' from the list above. 
    Keep in mind the amount of time between the timestamps when considering how far to move. The coordinates are in meters, so a jump of 0.1 corresponds to 10 centimeters. In general,
    try to use v-shaped motions since you are commanding the "head" of the robot on the "neck" of its arm.
    \n\nRespond with only the list-of-lists of waypoints, and no other text. Start with the character `[`"""
    # Make the API call

    # print(prompt)
    completion = client.chat.completions.create(
        model="gpt-4o",  # Adjust model if needed
        messages=[{"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": prompt}],
        temperature=0
    )
    # Extract the waypoints from the response
    waypoints_text = completion.choices[0].message.content
    # print(waypoints_text)
    # print(extract_waypoints(waypoints_text))
    try: 

        waypoints = eval(extract_waypoints(waypoints_text))
        print("successfully got waypts from gpt")
        return waypoints
    except: 
        print("couldn't do it, try again")
        # print(waypoints_text)
        return [-1]
    # Print or process the waypoints
    

if __name__== "__main__":
    from audio_analysis import analyze_audio
    tstamps, timing = analyze_audio("skutababa.mp3")
#     tstamps = """[ 0.34829932  0.81269841  1.10294785  1.40480726  1.71827664  2.03174603
#   2.33360544  3.55265306  3.86612245  4.16798186  4.46984127  4.78331066
#   5.08517007  5.39863946  5.70049887  6.31582766  8.45206349  9.68272109
#  10.14712018 10.5999093  10.90176871 11.2152381  11.51709751 11.83056689
#  12.1324263  12.58521542 13.04961451 13.3630839  13.66494331 15.04653061
#  16.10303855 16.41650794 16.72997732 17.03183673 17.48462585 17.94902494
#  18.26249433 18.55274376 18.86621315 19.16807256 19.94594104 20.39873016pytho
#  20.70058957 20.96761905 21.31591837 21.93124717 22.39564626 22.84843537
#  23.41732426 24.06748299 24.84535147 25.29814059 25.86702948 26.8306576
#  27.28344671 28.35156463 29.73315193]"""
    waypts = queryGPT_waypoints(tstamps)
    print(len(waypts))
    print(len(tstamps))
