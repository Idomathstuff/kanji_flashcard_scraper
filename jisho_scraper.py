from bs4 import BeautifulSoup
import requests


def char_is_hiragana(c) -> bool:
  return u'\u3040' <= c <= u'\u309F'

def char_is_kanji(c) -> bool:
  return u'\u4E00' <= c <= u'\u9FAF'

def kanji_list_make():
  kanji_q = []
  file = open('input.txt', 'r', encoding='utf-8').read()
  fl = open('kanji_list.txt', 'w', encoding='utf-8')
  for char in file:
    if char not in kanji_q and char_is_kanji(char):
      kanji_q.append(char)
      fl.write(char + '\n')
  fl.close()

def main():
  out = open('pop.txt', 'w', encoding='utf-8')
  for kanji in file[0:20]:
    word1 = {'word': '', 'hirigana': '', 'def': ''}
    word2 = {'word': '', 'hirigana': '', 'def': ''}
    word3 = {'word': '', 'hirigana': '', 'def': ''}
    url = 'https://jisho.org/search/*'+kanji+'*%20%23common'
    result = requests.get(url)
    soup = BeautifulSoup(result.content.decode('utf-8', 'ignore'), "html.parser")
    tmp1 = soup.find_all('span',class_="text")
    
    def furigana(i):
      furigana = ''
      for char in str(tmp1[i].parent.find('span', class_='furigana')):
        if char_is_hiragana(char):
          furigana+=char
      return furigana

    text = lambda i: tmp1[i].text.strip(' \n')
    furi = furigana
    meaning = lambda i: str(tmp1[i].parent.parent.parent.parent.find('span', class_='meaning-meaning').text)
    try:
      word1['word'],word1['hirigana'],word1['def'] = text(1),furi(1),meaning(1)
      out.write(kanji + '-' + word1['word'] + ',' + word1['hirigana'] + ','+ word1['def']+'\n')
    except:
      print(kanji)
      pass
    try:
      word2['word'],word2['hirigana'],word2['def'] = text(2),furi(2),meaning(2)
      out.write(word2['word'] + ',' + word2['hirigana'] + ','+ word2['def']+'\n')
    except:
      out.write('\n')
      pass
    try:
      word3['word'], word3['hirigana'], word3['def'] = text(3), furi(3), meaning(3)
      out.write(word3['word'] + ',' + word3['hirigana'] + ',' + word3['def'] + '\n\n')
    except:
      out.write('\n')
      pass

if __name__=='__main__':
  kanji_list_make()
  file = open("kanji_list.txt", "r", encoding="utf-8").read().split()
  main()
