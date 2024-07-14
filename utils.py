from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from oletools.olevba import VBA_Parser, VBA_Scanner, detect_suspicious, detect_patterns, detect_autoexec
from oletools.olevba import VBA_Parser, VBA_Scanner, detect_suspicious, detect_patterns, detect_autoexec
from oletools.olevba import VBA_Parser
#import obfuscation_detection as od
from oletools.olevba import VBA_Parser, VBA_Scanner, detect_suspicious, detect_patterns, detect_autoexec
from oletools.olevba import detect_patterns
import networkx as nx
import matplotlib.pyplot as plt
import re
import os


api_key = 'API-KEY'
client = MistralClient(api_key=api_key)
model = "mistral-large-latest"

def generate_content(vba_code,prompt):
    
    prompt = prompt+'\n'+'VBA Code:\n'+vba_code
    # Split prompt into messages for Mistral AI
    messages = [ChatMessage(role="user", content=prompt)]
    
    # Call Mistral AI API to generate the rewrite recommendations
    chat_response = client.chat(model=model, messages=messages)
    
    # Extract the rewrite recommendations from Mistral AI's response
    recommendations = chat_response.choices[0].message.content.strip()
    
    return recommendations

def get_vbaCode(file_name):
    vbaparser = VBA_Parser(file_name)

    vba_codes = []

    for (filename, stream_path, vba_filename, vba_code) in vbaparser.extract_macros():
        if any(line.strip() and not line.strip().startswith('Attribute') for line in vba_code.split('\n')):
            # print('-'*79)
            # print('Filename    :', filename)
            # print('OLE stream  :', stream_path)
            # print('VBA filename:', vba_filename)
            # print('- '*39)
            # print(vba_code)

            vba_codes.append(vba_code)
    # print(vba_codes)
    return vba_codes

def get_suspicious_keywords(vba_code):
    suspicious_keywords = detect_patterns(vba_code)
    suspicious_keywords_list = []
    if suspicious_keywords:
        print('Suspicious VBA keywords found:')
        for keyword, description in suspicious_keywords:
            suspicious_keywords_list.append((keyword, description))
    else:
        print('Suspicious VBA keywords: None found')
    return suspicious_keywords_list

def get_suspicious_patterns(vba_code):
    patterns = detect_patterns(vba_code)
    patterns_list = []
    if patterns:
        print('Patterns found:')
        for pattern_type, value in patterns:
            patterns.append((pattern_type, value))
    else:
        print('Patterns: None found')
    return patterns_list

def drawDiagram(recommendations):
    steps = re.findall(r'\d+\.\s(.*?)(?=\s*\d+\.|\Z)', recommendations, re.DOTALL)
    G = nx.DiGraph()


    for i in range(len(steps) - 1):
        step_current = steps[i][:40] 
        step_next = steps[i + 1][:40]
        G.add_edge(step_current, step_next)

    pos = nx.spring_layout(G, k=0.8) 

    # Draw the graph
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", node_shape="s", linewidths=0.5, edge_color='grey', font_color='black')
    # Save the graph as an image
    plt.title("Flow Diagram of Subroutine 'CalculateTotalSales'")
    plt.tight_layout()
    print('Diagram func called')
    relative_path = 'static'
    os.makedirs(relative_path, exist_ok=True)
    plt.savefig(os.path.join(relative_path, 'flow_diagram.png'))
