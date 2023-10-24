# Signal Viewer
Task 1✅
Introduction: Monitoring the vital signals is a crucial aim in any ICU room.
Description: Using Python and Qt, develop a desktop application that illustrates multi-port, multi-channel signal viewer
that has the following features:
- The user can browse his PC to open any signal file. Each group will need to provide samples from any three different
medical signals (e.g. ECG, EMG, EEG,...etc). Each signal type should have an example for normal signal and abnormal
signal.
- Your application should contain two main identical graphs. The user can open different signals in each graph. i.e. each
graph has to have its own controls. The user can run each graph independently or link both graphs via a button in the
UI. When the graphs are linked, the two graphs must display the same time frames, signal speed, and same viewport if
zoomed or panned (i.e. if the user zoom on one graph, the other graph should apply the same exact zoom as well). If
the link of the two graphs is disabled, then each graph can run its signals independently.
- In any of the two graphs, when the user opens a signal file, the signal should show up in the cine mode (i.e. a running
signal through time, similar to the one you see in the ICU monitors). Do NOT open a signal in a static mode. If the
signal ends, there should be a rewind option to either stop the signal or start running it again from the beginning.
- The use can manipulate the running signals through UI elements that provide the below function:
• Change color,
• Add a label/title for each signal,
• Show/hide,

• Control/customize the cine speed,
• Zoom in/out,
• Pause/play/rewind(on/off),

• Scroll/Pan the signal in any direction (left, top, right, bottom). Scroll is performed through sliders, and pan is
performed through the mouse movements.
• Move any signal from one graph to the other.
During these manipulations, you need to take care of the boundary conditions! Intuitively, no scroll/pan should be
allowed before your signal starts or after it ends or above its maximum values or below its minimum values. No user
expects to see an empty graph coz he scrolled the signal too much to the top for example. Note: Ofcourse, all
manipulations will be applied on all the opened signals (viewed or hidden).
- Exporting & Reporting: For the sake of reporting, the user can construct a report of one or more snapshots for the
graphs sent to the report along with some data statistics on the displayed signals to a pdf file. You need to generate
the pdf contents via the code. i.e. Do NOT take a snapshot image and convert it to a pdf file!
• Data statistics can be mean, std, duration, min and max values for each signal. These numbers should be
organized in a nice table in the pdf file. The report itself should be organized to have a nice layout. The report can
be single or multi-page. Prepare samples of your reports for different number of signals and snapshots.
