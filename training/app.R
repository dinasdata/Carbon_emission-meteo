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
    data = data$carbon_dioxyde[1:input$size]
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
output$plot = renderPlot({
    req(input$dataset)
    req(input$size)
    ggplot()+
    geom_point(mapping = aes(x = dataset(),y = real_pred()(dataset())$linear_regression),color = "red")+
    geom_point(mapping = aes(x = dataset(),y = real_pred()(dataset())$lasso_regression),color = "blue")+
    geom_point(mapping = aes(x = dataset(),y = real_pred()(dataset())$polynomial_regression),color = "black")+
    geom_point(mapping = aes(x = dataset(),y = real_pred()(dataset())$support_vector_machine),color = "green")+
    theme_light()
})

}
shinyApp(ui,server) 