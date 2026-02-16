library("jsonlite")
library("httr")
library("shiny")
library("shinydashboard")
library("readr")
library("ggplot2")
library("dplyr")



ui = dashboardPage( 
dashboardHeader(title = "Temperature Prediction "),
dashboardSidebar(fileInput("datasete","Upload here carbon dioxyde data")),
dashboardBody(
    fluidRow(
        box(width = 8,
        plotOutput("plot"),downloadButton("down","Download raw data",class = "btn-success")),
        box(width = 4,title = "Control",sliderInput("size","Select sample size",max = 20,min = 1,value = 10),
        actionButton("btn","Refresh size",class = "btn-primary"))
    )
)
)
server = function(input,output) {
ds = reactive({data = read_csv(input$datasete$datapath)
return(data)})
dataset = reactive({
    req(input$datasete)
    data = ds()$carbon_dioxyde[1:input$size]
    return (data)
})
observeEvent(input$btn,{
    updateSliderInput(inputId = "size",max = length(ds()$carbon_dioxyde),min = 1,value = 5)
})
predict = reactive({
prediction = function(x){
#setting url
url = "http://127.0.0.1:8000/predict/"
#sending API request 
body = list(carbon_dioxyde = x)
api_var = httr::POST(url,body = body,encode = "json")
#converting int json format for content reading
api_values = base::rawToChar(api_var$content)
#getting data
data = fromJSON(api_values)
return (data)}
})
real_pred = reactive({
pred_all = function(data){
lr = c(0,nrows = 4)
lasso = c(0,nrows = 4)
poly = c(0,nrows = 4)
svr = c(0,nrows = 4)
for (i in 1:(length(data))){
lr[i] = (predict()(data[i])$"Linear regression prediction")
lasso[i] = (predict()(data[i])$"Lasso regression prediction")
poly[i] = (predict()(data[i])$"Polynomial regression prediction")
svr[i] = (predict()(data[i])$"svr prediction")
}
result = data.frame(linear_regression = lr,lasso_regression = lasso, polynomial_regression = poly, support_vector_machine = svr)
return(result)
}

})
linreg = reactive({
    real_pred()(dataset())$linear_regression
})
lassoreg = reactive({
    real_pred()(dataset())$lasso_regression
})
polyreg = reactive({
    real_pred()(dataset())$polynomial_regression
})
svr = reactive({
    real_pred()(dataset())$support_vector_machine
})
observe({
    print(length(linreg()))
    print(length(lassoreg()))
    print(length(polyreg()))
    print(length(svr()))
})
output$plot = renderPlot({
    req(input$datasete)
    req(input$size)
    ggplot()+
    geom_point(mapping = aes(x = dataset(),y = linreg(),fill = "Linear Regression"),color = "red")+
    geom_line(mapping = aes(x = dataset(),y = linreg()),color = "red")+
    geom_point(mapping = aes(x = dataset(),y = lassoreg(),fill = "Lasso Regression"),color = "blue")+
    geom_line(mapping = aes(x = dataset(),y = lassoreg()),color = "blue")+
    geom_point(mapping = aes(x = dataset(),y = polyreg(),fill = "Polyomial Regression"),color = "black")+
    geom_line(mapping = aes(x = dataset(),y = polyreg()),color = "black")+
    geom_point(mapping = aes(x = dataset(),y = svr(),fill = "Support Vector Machine Regressor"),color = "green")+
    geom_line(mapping = aes(x = dataset(),y = svr()),color = "green")+
    labs(title = "Predicted temperature by ML models",x = "indexes",y = "temperature(°C)",fill = "Model type")+
    theme_light()  
    })
output$down = downloadHandler(
    filename  = function(){
        paste("predicted.csv")
    },
    content = function(file){   
        write.csv(real_pred()(dataset()),file,row.names = FALSE)
    }
)
}
shinyApp(ui,server) 