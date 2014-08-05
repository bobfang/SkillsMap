from wordlist import WordList
from ..data import utils
import itertools

def words(countries=True, states=True, counties=True, cities=True):
  if not utils.data_downloaded('gazeteer'):
    raise Exception("Gazeteer data files not found.")
  return Gazeteer(countries, states, counties, cities)

class Gazeteer(WordList):
  
  misc = ['north','east','south','west','northeast','northwest','southeast','southwest', # directions
          'midwest']

  def load_gaz(self, filename, cols):
    data = utils.load_file('gazeteer', filename, cols, comment="#")
    flat = list(itertools.chain.from_iterable(data))
    res = set()
    for item in flat: res.update(item.lower().split())
    return res

  def __init__(self, countries, states, counties, cities):
    self.locwords = set()
    self.locwords.update(self.misc)
    if countries: self.locwords |=  self.load_gaz('countries.tsv',[4,1])
    if states: self.locwords |=  self.load_gaz('usa_states.tsv',[2,10])
    if counties: self.locwords |= self.load_gaz('usa_counties.tsv', [2])
    if cities: self.locwords |= self.load_gaz('usa_cities.tsv',[2])

  def __contains__(self, text):
    return text.lower() in self.locwords
