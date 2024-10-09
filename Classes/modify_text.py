from typing import Protocol
import re


class TextGenerator(Protocol):
    def __call__(self, input:str)->str:
        ...

generator_identity:TextGenerator = lambda x: x 

class generator_counter:
    def __init__(self, initial, increase):
        self.increase = increase
        self.value:int = initial-increase
    
    def __call__(self, _x:str)->int:
        self.value += self.increase
        return self.value
    
# Function that finds and creates TextGenerators for each wildcard. returns list of TextGenerators and search strings
def get_text_generators(pattern:str) -> tuple[[list[str], list[TextGenerator]]]:
    """Creates a list of required text patterns and TextGenerators\n    
    '*' means wildcard \n
        if pattern is\n
            abc * efg\n
        and text is \n
            abc lorem efg\n
        the pattern will match and the wildcard will be lorem\n
    '{d:d}' means counter where the first 'd' is the initial value and the second 'd' is the increment (d can only be integers >=0)\n
        if pattern is \n
            abc {1:3} efg\n
        and text is \n
            abc lorem efg\n
        the pattern will match and the wildcard will be 1 and increment to '{4,3}'\n
    Args:
        pattern (str): text representing pattern to match

    Returns:
        _type_: tuple with two list the first is the values expected to be in a string that is going to be modified, the second is a list of the TextGenerators
    """
    search_regex = "(°/0)|({\\d+:\\d+})"
    pattern = pattern.replace("*", "°/0")
    iter = re.finditer(search_regex, pattern)
    end = [m.start(0) for m in iter] + [len(pattern)]
    iter = re.finditer(search_regex, pattern)
    start = [0] + [m.end(0) for m in iter]
    # get static patterns
    static_patterns = [pattern[a:b] for a,b in zip(start,end)]
    
    wildcards = re.findall(search_regex, pattern)
    generators:list[TextGenerator] = []
    
    for wildcard in wildcards:
        if re.match("°/0",wildcard[0]):
            generators.append(generator_identity)
        if re.match("{\\d+:\\d+}",wildcard[1]):
            generators.append(generator_counter(*map(int,wildcard[1][1:-1].split(":"))))
    
    return static_patterns ,generators

def elements_in_order(s: str, lst: list) -> bool:
    start_idx = 0    
    for elem in lst:
        found_idx = s.find(elem, start_idx)
        if found_idx == -1:
            return False
        start_idx = found_idx + len(elem)
    
    return True

def extract_between(alpha, lst):
    result:list[str] = []
    start_pos = 0  # Posición inicial para la búsqueda
    # Iterar por pares consecutivos en la lista
    for i in range(len(lst) - 1):
        first, second = lst[i], lst[i + 1]
        
        # Encontrar el índice del primer string
        start_index = alpha.find(first, start_pos)
        if start_index == -1:
            return None

        # Mover el índice después del primer string
        start_index += len(first)

        # Encontrar el índice del segundo string
        end_index = alpha.find(second, start_index)
        if end_index == -1:
            return None

        # Extraer la subcadena entre los dos strings
        result.append(alpha[start_index:end_index])

        # Actualizar la posición inicial para la siguiente búsqueda
        start_pos = end_index

    return result


# Function that creates the text given a string patterns
def generate_text(original:str, target:str, statics:list[str], generators:list[TextGenerator]):
    """replaces the text of original with target using generators (the replace variable is $n) where n is the position of the wildcard

    Args:
        original (str): _description_
        target (str): _description_
        statics (list[str]): _description_
        generators (list[TextGenerator]): _description_

    Returns:
        _type_: _description_
    """
    if not elements_in_order(original, statics):
        return original
    starting_index = 0
    # find the string between each statics
    wildcard_values = extract_between(original, statics)
    replacements = [gen(s) for gen,s in zip(generators, wildcard_values)]
    
    replacement_target = target
    for i in range(len(generators)):
        replacement_target = replacement_target.replace(f"${i}", str(replacements[i]))
    return replacement_target
    
    

if __name__ == "__main__":
    pattern = u"*¿abc asdf * qwerwe * zcvzxv* {1:2} ñlkñl"
    example_original = u"lorem abc asdf ipsum qwerwe yuyun zcvzxvgolian gamma ñlkñl"
    example_target = u"yunaml"
    statics, generators = get_text_generators(pattern)
    # Test for get_text_generators
    

    