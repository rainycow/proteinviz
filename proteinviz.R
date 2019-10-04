library(shiny)
library(plotly)
library(htmlwidgets)
library(ggplot2)
#install.packages("shinythemes")

setwd('/Desktop/')
data = read.csv('fdr5_proteinlist.csv')


library(shiny)

# Define UI for random distribution app ----
ui <- fluidPage(
  theme = shinythemes::shinytheme("flatly"),
  
  # App title ----
  titlePanel("How many proteins do we lose?"),
  
  br(),
  # Sidebar layout with input and output definitions ----
  sidebarLayout(
    
    # Sidebar panel for inputs ----
    sidebarPanel(
      # br() element to introduce extra vertical spacing ----
      # sidebarLayout(
        
        # Define the sidebar with one input
     #   sidebarPanel(
          selectInput("sample", "Choose sample to examine:",
                      choices=colnames(data)[2:7]),
          hr(),
    
      # Input: Slider for the number of observations to generate ----
      sliderInput("n",
                  "Number of peptides to consider:",
                  value = 0,
                  min = 0,
                  max = 30,
                  step = 1)
      
    ),
    
    # Main panel for displaying outputs ----
    mainPanel(
      
      # Output: Tabset w/ plot, summary, and table ----
      tabsetPanel(type = "tabs",
                  tabPanel("Plot", plotOutput("barplot"))

      )
      
    )
  )
)

# Define server logic for random distribution app ----
server <- function(input, output) {
  # original protein list
  original <- reactive({
    x = data[input$sample]
    colnames(x) = 'Count'
    x$ProteinName = data$ProteinName
    x
  })
  # filtered protein list
  filtered <- reactive({
   # data2 = data[input$sample][data[input$sample] >= input$n]
    data2 = data[data[input$sample] >= input$n,]
    data3 = setNames(as.data.frame(data2[input$sample]), 'Count')
    data3$ProteinName = data2$ProteinName
    data3
    })
  
  
  output$barplot <-renderPlot({
    #stack them together to see the difference 
  #  ggplot(data=original(),aes_string(x='ProteinName'))+
      ggplot() +
      geom_bar(data=original(), aes_string(x='ProteinName', y='Count'),stat="identity",alpha=.5,fill='lightblue',color='lightblue') +
      geom_bar(data=filtered(), aes_string(x='ProteinName', y='Count'),stat="identity",position ="identity",alpha=.5,fill='pink',color='pink') +
      labs(title=input$sample, y ="Count") 

  })
  
  
}

# Create Shiny app ----
shinyApp(ui, server)






