# This is an experimental new approach to subscriptions (visualization, table, etc.)

# Old way:
# gs.DETS = [qem07]
# gs.PLOT_Y = 'gc_diag_grid'
# gs.TABLE_COLS = [...]
# RE(ct())

# New way:
# d = [qem07]
# RE(count(d))
# ... and table and plot configure themselves automatically


from bluesky.callbacks import CallbackBase, LiveTable, LivePlot
import matplotlib.pyplot as plt

# This class will someday go int bluesky itself.
# We are just prototyping it for SIX here.
class BestEffortCallback(CallbackBase):
    def __init__(self):
        # internal state
        self.table = None
        self.figures = {}  # maps descriptor uid to (fig, axes)
        self.live_plots = {}  # maps descriptor uid to dict which maps data key to LivePlot instance
        self.start_doc = None

        # public options
        self.overplot = True
        self.truncate_table = False 
    
    def start(self, doc):
        print('You are running a', doc['plan_name'])
        self.start_doc = doc
    
    def descriptor(self, doc):
        if doc.get('name') == 'primary':
            columns = list(doc['data_keys'])
            self.table = LiveTable(columns)
            self.table('start', self.start_doc)
            self.table('descriptor', doc)
            fig_name = ' '.join(sorted(columns))
            fig = plt.figure(fig_name)
            if not fig.axes:
                # This is a apparently a fresh figure. Make axes.
                # The complexity here is due to making a shared x axis.
                for i in range(len(columns)):
                    if i == 0:
                        ax = fig.add_subplot(len(columns), 1, 1 + i)
                    else:
                        ax = fig.add_subplot(len(columns), 1, 1 + i, sharex=ax)
                fig.subplots_adjust()
                axes = fig.axes
                self.figures[doc['uid']] = (fig, axes)
            else:
                # Overplot on existing axes.
                axes = fig.axes
            self.live_plots[doc['uid']] = {}
            for y_key, ax in zip(columns, axes):
                # Are we plotting against a motor or against time?
                motors = self.start_doc.get('motors') or None
                if motors:
                    x_key = motors[0]
                live_plot = LivePlot(y=y_key, x=x_key, ax=ax)
                live_plot('start', doc)
                self.live_plots[doc['uid']][y_key] = live_plot

    def event(self, doc):
        self.table('event', doc)
        for y_key in doc['data']:
            live_plot = self.live_plots[doc['descriptor']][y_key]
            live_plot('event', doc)

    def stop(self, doc):
        self.table('stop', doc)
        for live_plots in self.live_plots.values():
            for live_plot in live_plots.values():
                live_plot('stop', doc)

    def clear(self):
        self.table = None
        self.live_plots.clear()
        self.figures.clear()
        self.start_doc = None


 
try:
    RE.unsubscribe(token)
except NameError:
    pass
B = BestEffortCallback()
token = RE.subscribe('all', B)
