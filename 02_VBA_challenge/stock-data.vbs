Sub StockData():

    'Loop through all of the years'
    Lastrow = Cells(Rows.Count, 1).End(xlUp).Row

    'Ticker Column'
    Cells(1, 9).Value = "Ticker"
    Cells(1, 10).Value = "Yearly Change"
    Cells(1, 11).Value = "Percentage Change"
    Cells(1, 12).Value = "Total Stock Volume"

    'Create array containing all Tickers'
    Dim tickersIndex As Integer
    tickersIndex = 2

    'Loop through all data points'

    For i = 2 To Lastrow

        'For each stock, find the first ticker index, the last ticker index,
        'the opening price, the closing price, and add up the volume'
        Dim currTicker As String
        Dim firstTickerIndex, lastTickerIndex As Integer
        Dim openPrice, closePrice, currVolume As Double
        
        currTicker = Cells(i, 1).Value

        'If the previous ticker is different from the current one, then assign the opening price,
        'save the index of the first ticker of a new stock, and restart the total volume
        If (Cells(i - 1, 1).Value <> currTicker) Then
            openPrice = Cells(i, 3).Value
            firstTickerIndex = i
            currVolume = Cells(i, 7).Value

            'Puts new Ticker down'
            Cells(tickersIndex, 9).Value = currTicker

        'If the next ticker is different from the current one, then assign the closing price
        'to a variable, and calculate yearly changes, percentage change, and stock volume
        ElseIf (Cells(i + 1, 1).Value <> currTicker) Then
            closePrice = Cells(i, 6).Value
            currVolume = currVolume + Cells(i, 7).Value

            'Yearly change from opening price at the beginning of a given year
            'to the closing price at the end of that year.
            Dim yearlyChange, percChange As Double
            yearlyChange = (Cells(i, 6).Value - Cells(firstTickerIndex, 3).Value)

            If (Cells(firstTickerIndex, 3).Value < > 0) Then
            	percChange = yearlyChange / Cells(firstTickerIndex, 3).Value
            Else
            	percChange = 0
            End If

            'Put yearly change, percentage change, and total volume down'
            Cells(tickersIndex, 10).Value = yearlyChange
            Cells(tickersIndex, 11).Value = Format(percChange, "Percent")
            Cells(tickersIndex, 12).Value = currVolume

            'Change color of yearly change to green if change is positive'
            If yearlyChange > 0 Then
            	Cells(tickersIndex, 11).Interior.ColorIndex = 4

            'Change color of yearly change to red if change is negative'
            Elseif yearlyChange < 0 Then
            	Cells(tickersIndex, 11).Interior.ColorIndex = 3
            End if

            tickersIndex = tickersIndex + 1

        ElseIf (Cells(i - 1, 1).Value = currTicker And Cells(i + 1, 1).Value = currTicker) Then
            currVolume = currVolume + Cells(i, 7).Value

        End If

    Next i

End Sub
