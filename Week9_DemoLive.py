import bokeh as bk
import bokeh.plotting
import bokeh.io
import bokeh.layouts
import pandas as pd
import bokeh.models as bmod
import statsmodels.formula.api as smf

bk.io.output_file('index.html', title = "Smoking vs. Lung Cancer, PS627 W2025")


smokingData = pd.read_csv('Table1_SmokingVsCancer.csv')

model1 = smf.ols('LungCancerPer100 ~ PercentSmokers', smokingData).fit()
model2 = smf.ols("LungCancerPer100 ~ UnemploymentRate", smokingData).fit()

plot = bk.plotting.figure(title = 'Smoking vs. Lung Cancer per 100k',
                          x_axis_label = 'Smoking Rates',
                          y_axis_label = 'Lung Cancer Per 100,000 People',
                          sizing_mode = "stretch_width")

xData = smokingData['PercentSmokers']
yData = smokingData['LungCancerPer100']
lineOfFit = model1.fittedvalues

plot.line(xData, lineOfFit, color = "red", legend_label = "Regression Line")
plot.legend.location = "top_left"
plot.legend.click_policy = 'hide'

plot.circle(xData, yData, size = 10)

regressionResults = model1.summary().tables[0].as_html()
regressionCoeff = model1.summary().tables[1].as_html()
regressionResultDiv = bmod.Div(text = regressionResults + regressionCoeff)


plot2 = bk.plotting.figure(title = 'Unemployment vs. Lung Cancer per 100k',
                          x_axis_label = 'Unemployment Rate',
                          y_axis_label = 'Lung Cancer Per 100,000 People',
                          sizing_mode = "stretch_width")

xData2 = smokingData['UnemploymentRate']
yData2 = smokingData['LungCancerPer100']
lineOfFit = model2.fittedvalues

plot2.circle(xData2, yData2, size = 10)
plot2.line(xData2, lineOfFit, color = "red")

regressionResults2 = model2.summary().tables[0].as_html()
regressionCoeff2 = model2.summary().tables[1].as_html()

regressionResults2 = regressionResults2.replace('simpletable', 'table table-bordered')
regressionResultDiv2 = bmod.Div(text = regressionResults2 + regressionCoeff2)

bk.plotting.save(bk.layouts.column(
    bk.layouts.row(
        bk.layouts.column(
            plot,
            regressionResultDiv,
            sizing_mode = "stretch_width"
        ),
        bk.layouts.column(
            plot2, 
            regressionResultDiv2,
            sizing_mode = "stretch_width"
        ),
    sizing_mode = "stretch_width"), sizing_mode = "stretch_width"))


