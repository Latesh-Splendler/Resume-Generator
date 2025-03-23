import google.generativeai as genai

genai.configure(api_key="AIzaSyDCR90AjklYFAoXyElm0ayV3eyKY-GpyWw")

models = genai.list_models()
for model in models:
    print(model.name)
