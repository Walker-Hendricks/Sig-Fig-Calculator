# I made this a long time ago for another project and just copied it over
# leave me alone plz

import re
from scipy.constants import mu_0, epsilon_0, pi, g, h, hbar, G, R, c, golden, k, N_A
from scipy.constants import physical_constants
from math import e
from sympy import I


lower_greek = [chr(ord_) for ord_ in range(ord(u"\U0001D6FC"), ord(u'\U0001d714')+1)]
del lower_greek[17]
lower_greek_key = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega']


upper_greek = [chr(ord_) for ord_ in range(ord(u'\U0001d6e2'), ord(u'\U0001d6fa')+1)]
del upper_greek[-8]
upper_greek_key = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega']


lower_eng = [chr(ord_) for ord_ in range(ord(u'\U0001d44e'), ord(u'\U0001d467')+1)]
lower_eng[7] = u'\u210e'
lower_eng_key = [chr(ord_) for ord_ in range(ord('a'), ord('z')+1)]


upper_eng = [chr(ord_) for ord_ in range(ord(u'\U0001d434'), ord(u'\U0001d44d')+1)]
upper_eng_key = [chr(ord_) for ord_ in range(ord('A'), ord('Z')+1)]


num = [chr(ord_) for ord_ in range(ord(u"\U0001D7E2"), ord(u"\U0001D7EB")+1)]
num_key = [chr(ord_) for ord_ in range(ord('0'), ord('9')+1)]

dic = lower_greek + upper_greek + lower_eng + upper_eng + num
key = lower_greek_key + upper_greek_key + lower_eng_key + upper_eng_key + num_key

letter_key = dict(zip(key, dic))



# The regex pattern for all Greek letters in LaTeX
greek_letters = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega', 'Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega']
greek_letter_pattern = '|'.join(greek_letters)

def transform_vars(vars):
    '''
        Transforms a list of variables to nice unicode characters.
        For dropdowns and value entries.
    '''
    # Regex to find Greek letters not followed by a space, an underscore, or the end of the string
    pattern = re.compile(r'\\(' + greek_letter_pattern + r')(?=\S)(?!_)')
    # Add a space after Greek letters if not followed by a space, underscore, or end of the string
    for count in range(len(vars)):
        vars[count] = pattern.sub(r'\\\1 ', vars[count])

    def transform_subscript(subscript):
        # Recursively transform the content within the subscript
        if subscript.startswith('{') and subscript.endswith('}'):
            subscript = subscript[1:-1]
            return '{' + transform_variable(subscript) + '}'
        else:
            return transform_variable(subscript)

    def transform_variable(var):
        pattern = re.compile(r'\\([a-zA-Z]+)(?:_(\{.*?\}|[a-zA-Z0-9]+))?')
        transformed_var = ''
        pos = 0
        while pos < len(var):
            match = pattern.match(var, pos)
            if match:
                base_var = match.group(1)
                subscript = match.group(2)
                if base_var in letter_key:
                    transformed_var += letter_key[base_var]
                else:
                    transformed_var += '\\' + base_var
                if subscript is not None:
                    transformed_var += '_'
                    transformed_var += transform_subscript(subscript)
                pos = match.end()
            else:
                # Transform single characters that are not part of LaTeX commands
                transformed_var += letter_key.get(var[pos], var[pos])
                pos += 1
        return transformed_var

    transformed_variables = [transform_variable(var) for var in vars]
    return transformed_variables



specialchars = {'i': ['Imaginary Unit', I], 'e': ["Euler's Number", e], '\\phi': ['Golden Ratio', golden], '\\pi': ['You know, THAT pi', pi], 'h': ['Planck Constant', h], '\\hbar': ['Reduced Planck Constant', hbar], 'k': ['Boltzmann Constant (J/K)', k], 'G': ['Gravitational Constant', G], 'c': ['Speed of Light in Vacuum', c], 'R': ['Ideal Gas Constant (J/mol*K)', R], 'N_A': ["Avogadro's Number", N_A], '\\mu_B': ['Bohr Magneton (J/T)', physical_constants['Bohr magneton'][0]], '\\mu_0': ['Magnetic Permeability', mu_0], '\\epsilon_0': ['Electric Permittivity', epsilon_0], 'g': ['Gravitational Acceleration (m/s)', g]}

# i + e + \phi + \pi + h + \hbar + k + G + c + R + N_A + \mu_B + \mu_0 + \epsilon_0 + g
def isspecialchar(equation):
    '''
    Checks if any of the identified variables are in the list of special characters above

    Returns a dictionary which is a subdictionary of specialchars above; used for a select menu.
    The first entry in the list is the name, the second is the value.
    '''
    specialdic = {}
    variables = re.findall(r'(?:\\[a-zA-Z]+(?:_\{[^}]+\}|\{[^}]+\}|_[a-zA-Zα-ωΑ-Ω0-9]+)?)|(?:[a-zA-Zα-ωΑ-Ω](?:_\{[^}]+\}|\{[^}]+\}|_[a-zA-Zα-ωΑ-Ω0-9]+)?)', equation)
    for var in variables:
        for key in specialchars.keys():
            if key == var:
                new_key = transform_vars([key])
                specialdic[new_key[0]] = specialchars[key]

    return specialdic


# Define allowed operations and symbols
allowed_operations = {
    # Basic arithmetic
    '+', '-', r'\cdot', '*', '/',

    # Fractions
    r'\frac',

    # Equality
    '=',

    # Parentheses, brackets, braces
    '(', ')', '[', ']', '{', '}', r'\left(', r'\right)', r'\left[', r'\right]', r'\left\{', r'\right\}',

    # Trigonometric functions
    r'\sin', r'\cos', r'\tan', r'\csc', r'\sec', r'\cot',

    # Hyperbolic trigonometric functions
    r'\sinh', r'\cosh', r'\tanh', r'\csch', r'\sech', r'\coth',

    # Logarithms
    r'\log', r'\ln',

    # Exponentials
    'e',

    # Greek letters (lowercase and uppercase)
    r'\alpha', r'\beta', r'\gamma', r'\delta', r'\epsilon', r'\zeta', r'\eta', r'\theta', r'\iota', r'\kappa', r'\lambda', r'\mu', r'\nu', r'\xi', r'\omicron', r'\pi', r'\rho', r'\sigma', r'\tau', r'\upsilon', r'\phi', r'\chi', r'\psi', r'\omega',
    r'\Alpha', r'\Beta', r'\Gamma', r'\Delta', r'\Epsilon', r'\Zeta', r'\Eta', r'\Theta', r'\Iota', r'\Kappa', r'\Lambda', r'\Mu', r'\Nu', r'\Xi', r'\Omicron', r'\Pi', r'\Rho', r'\Sigma', r'\Tau', r'\Upsilon', r'\Phi', r'\Chi', r'\Psi', r'\Omega',

    # English letters (lowercase and uppercase)
    *[chr(i) for i in range(ord('a'), ord('z')+1)],  # lowercase letters
    *[chr(i) for i in range(ord('A'), ord('Z')+1)],  # uppercase letters

    # Numbers
    *[str(i) for i in range(0, 10)],  # digits

    # Calculus
    r'\frac{d}{dx}', r'\frac{\partial}{\partial x}', r'\frac{\partial}{\partial y}', r'\frac{d}{dt}', r'\int', r'\iint', r'\iiint', r'\oint', r'\lim', r'\limsup', r'\liminf', r'\sum', r'\prod',

    # Infinity
    r'\infty',

    # Exponents and subscripts
    '^', '_',

    # Roots
    r'\sqrt'
}


def unallowedchar(input):
    '''
    Checks if a string has characters not allowed for user input (not in the set above)

    Returns EITHER None (if all elements in the LaTeX equation are allowed) OR a string displaying the elements rejected by this function
    '''
    # Checking all Latex patterns
    pattern = re.compile(r'\\sqrt(\[[^\]]+\])?{[^}]+}|\\frac{[^}]+}{[^}]+}|\\[a-zA-Z]+|[0-9]+|[a-zA-Z]|[+\-*/^_=(){}\[\]]|\\.')
    tokens = pattern.findall(input)
    invalid_elements = [token for token in tokens if token not in allowed_operations]
    if invalid_elements:
        return f'Error: invalid elements: {invalid_elements}'
    else:
        return None
