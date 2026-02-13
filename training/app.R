library("jsonlite")
library("httr")
library("shiny")
library("shinydashboard")
library("readr")
library("ggplot2")
library("dplyr")

ui = dashboardPage(
dashboardHeader(title = "Temperature Prediction "),
dashboardSidebar(fileInput("dataset","Upload here carbon dioxyde data")),
dashboardBody(
    fluidRow(
        valueBoxOutput("lr"),
        valueBoxOutput("lasso"),
        valueBoxOutput("poly"),
        valueBoxOutput("svr")
    ),
    fluidRow(
        box(width = 8,
        plotOutput("plot"),downloadButton("down","Download raw data",class = "btn-success")),
        box(width = 4,title = "Control",sliderInput("size","Select sample size",max = 20,min = 1,value = 10),selectInput("color","Select color",choices = c("black","red","green","blue")))
    )
)
)
server = function(input,output){
dataset = reactive({
    req(input$dataset)
    req(input$size)
    data = read_csv(input$dataset$datapath)
    #data = data$carbon_dioxyde[1:input$size]
    return (data)
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
datas = runif(10,min = 0.1,max = 0.9)
lr = c(0,nrows = length(datas))
lasso = c(0,nrows = length(datas))
poly = c(0,nrows = length(datas))
svr = c(0,nrows = length(datas))
for (i in 1:length(datas)){
lr[i] = (prediction(datas[i])$"Linear regression prediction")
lasso[i] = (prediction(datas[i])$"Lasso regression prediction")
poly[i] = (prediction(datas[i])$"Polynomial regression prediction")
svr[i] = (prediction(datas[i])$"svr prediction")
result = data.frame(linear_regression = lr,lasso_regression = lasso, polynomial_regression = poly, support_vector_machine = svr)
return(result)
}
})
output$plot = renderPlot({
    req(input$dataset)
    ggplot()+
    geom_line(mapping = aes(x = 1:input$size,y = predict(dataset())$linear_regression))
})
}
shinyApp(ui,server)