# To-do

## Get the collapsible tree up and running, based on examples.
If this fails, dump out JSON information for selected observation, let user
just scroll down the page.

## Determine relevant information and create relevant colour-coding functions

## Hook colour-coding functions into the drop-down box

## If possible, highlight selected observations
Make all other observations go slightly transparent when one is selected. Might
be quite difficult due to the way that the Gantt chart appears to be
jerry-rigged together (it appears to be a scatter plot, with one point at the
end of each box, and then the boxes drawn on top).
Maybe possible by redrawing (updating) the entire plot when one is selected?
Could change the colour scheme so that it includes one 'selected' key, which is
attributed to the selected value, and all other colours are reduced?

## Add in method of accessing any observations that were not scheduled
Need to check if this is the case for the current data (I think not), but even
if not, might be needed/useful for future schedules.

## Attempt to remove the Undo buttons from the Dash page
This might require some custom CSS
