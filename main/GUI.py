# Imports
import SigFigs as sf        # My classes for sig figs
import panel as pn          # Main GUI workhorse
import re                   # For variable isolation


# Necessary Functions




# Classes
class EqEntry:
    '''
    This class creates the first line of the widget: the equation entry the LaTeX output, and the dropdown menu for final variable selection.
    Both the LaTeX and dropdown widgets are updated upon equation, hence the singular on_update bound function.
    '''
    def __init__(self):
        # Creating the equation entry widget
        self.eq = pn.widgets.TextInput(name='Enter Equation (LaTeX Format)', placeholder='Enter LaTeX equation here...')
        self.eq.param.watch(self.on_update, 'value')

        # Creating the LaTeX widget
        self.latex = pn.pane.LaTeX('')

        # Creating the dropdown widget
        self.drop = pn.widgets.Select(name='Dependent Variable', options=['No item selected'])

        # Creating the layout
        column = pn.Column(self.eq, self.drop)
        self.layout = pn.Row(column, self.latex)


    def on_update(self, event):
        pass
    

# The next three classes use composition for each other.
# The first makes a widgetbox with checkboxes for different kinds of error
# The next creates a textbox for variable entry, adjacent to the widgetbox
# The third creates one of the secondary objects for every variable identified.
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

    The reason this is a subclass of ErrorBox is because the error box is included in this object.
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



# GUI Setup
