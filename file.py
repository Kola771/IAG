#Note: The openai-python library support for Azure OpenAI is in preview.
      #Note: This code sample requires OpenAI Python library version 0.28.1 or lower.
import os
import openai

openai.api_type = "azure"
openai.api_base = "https://interstisopenaiformation.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = '6ea9703016b54b9686e3a744defdd5c3'

message_text = [{"role":"system","content":"J'écris les histoires pour les mangas\nJe vais t'envoyer un liste contenant les noms de certains mangas et je veux que tu me fasses le résumé de leurs histoires"},{"role":"user","content":"donne-moi les résumés de tous ces mangas de la liste:\n- boruto"},{"role":"assistant","content":"Boruto :"},{"role":"user","content":"je veux les résumés des mangas  \n- Blue lock  \n- undead unluck"},{"role":"assistant","content":"Blue Lock :\n\nLe Japon est en proie à une crise footballistique sans précédent. L'équipe nationale n'a plus remporté de compétition depuis des années et la population commence à perdre tout intérêt pour ce sport. Pour y remédier, un projet ambitieux est lancé : créer une équipe capable de remporter la coupe du monde. Pour cela, un centre de formation est mis en place, le Blue Lock, dans lequel les meilleurs attaquants du pays sont rassemblés. Leur mission : devenir le meilleur buteur de l'équipe nationale et ainsi sauver le football japonais.\n\nUndead Unluck :\n\nUndead Unluck raconte l'histoire de Fuuko Izumo, une jeune fille qui possède un pouvoir étrange : tout ce qu'elle touche meurt instantanément. Un jour, elle rencontre un jeune homme immortel nommé Andy, qui a le pouvoir de donner la vie à tout ce qu'il touche. Ensemble, ils vont devoir affronter des ennemis dangereux et découvrir les secrets de leur pouvoir. Mais leur collaboration ne sera pas de tout repos, car Andy souhaite utiliser le pouvoir de Fuuko pour accomplir sa propre mission, qui consiste à tuer tous les immortels de la planète."}]

completion = openai.ChatCompletion.create(
  engine="gpt35",
  messages = message_text,
  temperature=0.5,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None
)

# Affichage de la réponse du chat
print(completion.choices[0].message.content)