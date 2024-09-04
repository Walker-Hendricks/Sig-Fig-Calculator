# Imports
import SigFigs as sf                                # My classes for sig figs
import fancytext as ft                              # My file for making text look nicer
import panel as pn                                  # Main GUI workhorse
import re                                           # For variable isolation
from sympy.parsing.latex import parse_latex         # Converting Latex input to Sympy




# Classes
class EqEntry:
    '''
    This class creates the first line of the widget: the equation entry the LaTeX output, and the dropdown menu for final variable selection.
    Both the LaTeX and dropdown widgets are updated upon equation, hence the singular on_update bound function.
    '''
    def __init__(self):
        # Creating the equation entry widget
        self.eqbox = pn.widgets.TextInput(name='Enter Equation (LaTeX Format)', placeholder='Enter LaTeX equation here...')
        self.eqbox.param.watch(self.on_update, 'value')

        # Creating the LaTeX widget
        self.latex = pn.pane.LaTeX('')

        # Creating the dropdown widget
        self.drop = pn.widgets.Select(name='Dependent Variable', options=['No item selected'])

        # Creating the layout
        column = pn.Column(self.eqbox, self.drop)
        self.layout = pn.Row(column, self.latex)


    def on_update(self, event):
        # Getting the raw equation for LaTeX
        self.raw_equation = fr'{self.eqbox.value}'
        variables = re.findall(r'(?:\\[a-zA-Z]+(?:_\{[^}]+\}|\{[^}]+\}|_[a-zA-Zα-ωΑ-Ω0-9]+)?)|(?:[a-zA-Zα-ωΑ-Ω](?:_\{[^}]+\}|\{[^}]+\}|_[\\a-zA-Zα-ωΑ-Ω0-9]+)?)', self.raw_equation)
        
        # Getting the right LaTeX output
        latex_pattern = re.compile(r'\\(' + ft.greek_letter_pattern + r')(?=\S)(?!_)')
        new_equation = latex_pattern.sub(r'\\\1 ', self.raw_equation)
        self.latex.object = new_equation

        # Getting the options for the dropdown menu
        variables = ft.transform_vars(variables)            # Making vars look nice
        self.unique_variables = []                          # Use a list to maintain order 
        seen = set()                                        # Use a set to ensure variable uniqueness
        for var in variables:                               # Ensuring unique variables
            if var not in seen:
                self.unique_variables.append(var)
                seen.add(var)
        
        # Setting new dropdown menu
        self.drop.options = ['No item selected'] + self.unique_variables



class ErrorBox:
    '''
    This class defines the WidgetBox containing possible errors.
    '''
    OPTIONS = ['Meter Stick Reading Error', 'Meter Stick End Error', 'Digital Reading Error', 'ADC Error', 'Known Mass Error']

    def __init__(self):
        self.meas = 0

        # Creating checkbox widget
        self.checkbox = pn.widgets.CheckBoxGroup(options=self.OPTIONS)

        # Function that activates on checkbox change:
        self.checkbox.param.watch(self.checkbox_callback, 'value')

        # Creating WidgetBox format
        self.box = pn.WidgetBox('### Errors', self.checkbox)

    
    def checkbox_callback(self, event):
        '''
        This method is enacted any time the checkbox group is updated. I.e., any time a checkbox is checked, this method happens.
        '''
        # Clear previous error
        self.err = 0
        self.errs = [0, 0, 0, 0, 0]
        # Iterate through all checkboxes
        for item in event.new:
            method_name = f'{item.replace(' ', '_')}'
            getattr(self, method_name)
        
        # Getting total final error
        for item in self.errs:
            self.err += item
    

    def Meter_Stick_Reading_Error(self):
        self.errs[0] = 0.05         # Error in CENTIMETERS!


    def Meter_Stick_End_Error(self):
        self.errs[1] = 0.1          # Error in CENTIMETERS!


    def Digital_Reading_Error(self):
        last_digit = self.meas.lsd
        self.errs[2] = 1 * 10**(last_digit)


    def ADC_Error(self):
        self.errs[3] = 0.005 * self.meas


    def Known_Mass_Error(self):
        self.errs[4] = 0.05 * self.meas


class EntryItem:
    '''
    This class defines how variables are entered into text boxes. Multiple of these will be created, one for every variable.
    '''

    def __init__(self, var_name):
        # Creating associated error box
        self.errbox = ErrorBox()

        # Creating variable text box
        self.varbox = pn.widgets.TextInput(name=var_name, min_width=80, width_policy='max', width = 80, max_width = 80)

        self.varbox.param.watch(self.text_callback, 'value')

        # Creating uncertainty text box
        self.uncertainty = pn.widgets.TextInput(name="\u00B1", min_width=80, width_policy='max', width = 80, max_width = 80)

        # Creating the layout
        column = pn.Column(self.varbox, self.uncertainty)
        self.layout = pn.Row(column, self.errbox)


    def text_callback(self):
        # Setting the errorbox's measurement to the entered measurement
        self.errbox.meas = sf.SigFig(self.varbox.value)
        self.errbox.checkbox_callback()
        self.uncertainty.value = self.errbox.err


class VarEntries:
    '''
    This class outlines how to set up all of the EntryItem objects for every detected variable.
    '''
    def __init__(self):
        self.eqEntry = EqEntry()
        # Once the drop box has a selection, the entries are generated
        self.eqEntry.drop.param.watch(self.generate_entries, 'value')


    def generate_entries(self):
        # Creating a cleaner name for the variables
        vars = self.eqEntry.unique_variables
        # Removing whatever is selected in the dropdown
        vars.remove(self.eqEntry.drop.value)
        # Creating a column to store all of the EntryItem widgets
        boxes_column = pn.Column()

        # Keeping track of EntryItems as they are created
        self.entryItems = {}

        # This next bit ensures that the EntryItem objects come in two columns
        length = len(vars) // 2
        rem = len(vars) % 2
        indx = 0
        for i in range(length):
            item1 = EntryItem(vars[indx])
            item2 = EntryItem(vars[indx+1])
            boxes_column.append(pn.Row(item1.layout, item2.layout))
            self.entryItems[vars[indx]] = item1
            indx += 2

        # Dealing with remaining boxes (not even multiples of 2)
        if rem == 1:
            boxes_column.append(pn.Row(EntryItem(vars[indx]).layout))
            self.entryItems.append(EntryItem(vars[indx]).layout)

        self.layout = pn.Column(EqEntry.layout, boxes_column)





class SigFigCalculator:
    
    def __init__(self):
        self.varEntries = VarEntries()
        # Creating the button for calculation
        self.button = pn.widgets.Button(name='Calculate', button_type='success')
        # Creating the LaTeX pane to show the solution
        self.solution_pane = pn.pane.LaTeX('')

        # Binding the button the buttonClick method
        pn.bind(self.buttonClick, self.button, watch=True)


    def buttonClick(self):
        pass


# GUI Setup
