Attribute VB_Name = "이동평균"
Option Explicit
Private start_row, end_row As Integer
Private page, page_count, page_num As Integer
Private MA(2) As Integer
Private long_cnt, short_cnt As Integer
Private arPage() As Variant

Sub start()
    Dim i As Integer
    Range(Cells(21, 3), Cells(200, 200)).ClearContents
    page_count = Sheet1.Cells(8, 10).Value
    If Sheet1.Cells(20 + page_count, 2) = "" Then
        MsgBox ("난수 생성을 먼저 하세요")
        Exit Sub
    End If
    
'    ReDim arPage(1 To page_count)
    
'    For i = 1 To page_count
'        arPage(i) = Int(Rnd * 145) + 1
'        Debug.Print "intNum" + Str(i) + "=" + Str(arPage(i))
'    Next i
    page = 1
    
    For i = 1 To page_count
        page_num = Sheet1.Cells(20 + i, 2).Value
        Call 찾기(page_num)
        page = page + 1
    Next i
    
    Worksheets(1).Activate
    
    
End Sub

'Sub rotate()
'    'Debug.Print "page", page
'
'    If page < page_count Then
'        page = page + 1
'        Call 찾기
'        Debug.Print page
'    Else
'        Call 종료
'    End If
'
''    Do
''        page = page + 1
''        Call 찾기
''    Loop Until page = page_count
'
'End Sub


Sub 찾기(page_num)
    Dim i, j, last As Integer
           
    Worksheets(page_num).Activate
    Dim start_date, end_date As Date
    last = Range("A10000").End(xlUp).Row
           
    start_date = Sheet1.Cells(8, 3)
    end_date = Sheet1.Cells(10, 3)
    start_row = 0
    end_row = 0
    
    For i = 2 To last
        If start_date = Cells(i, 1) Then
            start_row = Cells(i, 1).Row
            'Debug.Print start_row
            For j = start_row To last
                If end_date = Cells(j, 1) Then
                    end_row = Cells(j, 1).Row
                    
                    GoTo pass:
                End If
            Next j
        End If
        
    Next i
pass:
    If start_row = 0 Or end_row = 0 Then
        Exit Sub
    End If

'    Dim c As Range
'    With Range("A1:A1000")
'        Set c = .Find(Sheet1.Cells(8, 3), Lookat:=xlPart, LookIn:=xlFormulas) ''''''''''Sheet1.Cells(8, 3) 시작일
'
'        If c Is Nothing Then
'            Call rotate
'
'        ElseIf Not c Is Nothing Then
'            start_row = c.Row
'            Debug.Print (start_row)
'        End If
'    End With
'
'    With Range("A1:A1000")
'        Set c = .Find(Sheet1.Cells(10, 3), Lookat:=xlPart, LookIn:=xlFormulas) ''''''''''''Sheet1.Cells(10, 3) 종료일
'
'        If c Is Nothing Then
'            Call rotate
'
'        ElseIf Not c Is Nothing Then
'            end_row = c.Row
'            Debug.Print (end_row)
'            page = page + 1
'        End If
'    End With
    
    Call cal_ma
    
End Sub

Sub cal_ma()
    
    Range("G:T").Clear
    
    Dim r As Range
    
    MA(1) = Sheet1.Cells(8, 7).Value
    MA(2) = Sheet1.Cells(9, 7).Value
        
    Dim i As Integer
    Dim j As Integer
    
    For j = 1 To 2
        For i = start_row - 1 To end_row - MA(j)
            If Range("E" & i + MA(j)) = "" Then
                Exit For
            End If
            Set r = Range("E" & i & ":E" & i + MA(j))
            Cells(i + MA(j), j + 6).Value = Application.Sum(r) / r.Cells.Count
        Next i
    Next
    
    Call long_short

End Sub

Sub long_short()
    Dim i As Integer
    
    long_cnt = 0
    short_cnt = 0
    
    '''골든크로스 & 데드 크로스
    For i = start_row + MA(2) - 1 To end_row
    
        If Cells(i, 7).Value > Cells(i, 8).Value Then
            Cells(i, 9).Value = 1
        Else
            Cells(i, 9).Value = 2
        End If
        
    Next i
        
    '''매수 매도 포인트
    For i = start_row + MA(2) To end_row
        If Cells(i, 9).Value + Cells(i - 1, 9).Value = 3 Then
            If Cells(i, 9).Value = 1 And Cells(i + 1, 9) <> "" Then
                long_cnt = long_cnt + 1
                Cells(i + 1, 10).Value = "매수진입"
            ElseIf Cells(i, 9).Value = 2 And Cells(i + 1, 9) <> "" Then
                Cells(i + 1, 10).Value = "매도진입"
                short_cnt = short_cnt + 1
            End If
            
        End If
    Next i
    
    If short_cnt = 0 Or long_cnt = 0 Then
'        page = page - 1
        Exit Sub
    End If
    'Debug.Print end_row
    'Range("A" & end_row).Offset(1, 9).Clear
    
    Call cal
        
End Sub

Sub cal()
    Dim i, p, j As Integer
    Dim open_price, close_price As Single
    Dim profit, tot_Profit As Single
    Dim arProfit() As Single
    Dim trade_cnt As Integer
    Dim ave As Double
    Dim fee As Single
    
    fee = 1 - Sheet1.Cells(10, 7).Value
    trade_cnt = long_cnt + short_cnt
    ReDim arProfit(1 To trade_cnt)
    
    
    i = start_row
    tot_Profit = 1
    p = p + 1
    
    Do
        open_price = 0
        close_price = 0
        profit = 0
        j = 1
        
        
        If Cells(i, 10).Value = "매수진입" Then
            tot_Profit = tot_Profit * fee
            open_price = Cells(i, 2).Value
            close_price = Cells(i, 5).Value
            profit = (close_price / open_price) - 1
            tot_Profit = tot_Profit * (profit + 1)
            'Debug.Print tot_Profit
            
            Cells(i, 11).Value = open_price
            Cells(i, 12).Value = profit
            Cells(i, 13).Value = tot_Profit
            
            If Cells(i + 1, 10).Value = "매도진입" Or i = end_row Then
                Cells(i, 12).Value = profit * fee
                arProfit(p) = profit * fee
                p = p + 1
                
            Else
                Do
                    profit = (Cells(i + j, 5).Value / Cells(i + j - 1, 5).Value)
                    Cells(i + j, 12).Value = (Cells(i + j, 5).Value / open_price - 1)
                    tot_Profit = tot_Profit * profit
                    Cells(i + j, 13).Value = tot_Profit
                    j = j + 1
                Loop Until Cells(i + j, 10).Value = "매도진입" Or i + j - 1 = end_row
                Cells(i + j - 1, 13).Value = tot_Profit * fee
                arProfit(p) = (Cells(i + j - 1, 5).Value / open_price - 1) * fee
                p = p + 1
                
            End If
            
        ElseIf Cells(i, 10).Value = "매도진입" Then
            tot_Profit = tot_Profit * fee
            open_price = Cells(i, 2).Value
            close_price = Cells(i, 5).Value
            profit = (open_price / close_price) - 1
            tot_Profit = tot_Profit * (profit + 1)
            
            Cells(i, 11).Value = open_price
            Cells(i, 12).Value = profit
            Cells(i, 13).Value = tot_Profit
            
            If Cells(i + 1, 10).Value = "매수진입" Or i = end_row Then
                Cells(i, 12).Value = profit * fee
                arProfit(p) = profit * fee
                p = p + 1
                
            Else
                Do
                    profit = (Cells(i + j - 1, 5).Value / Cells(i + j, 5).Value)
                    Cells(i + j, 12).Value = open_price / Cells(i + j, 5).Value - 1
                    tot_Profit = tot_Profit * profit
                    Cells(i + j, 13).Value = tot_Profit
                    j = j + 1
                Loop Until Cells(i + j, 10).Value = "매수진입" Or i + j - 1 = end_row
                Cells(i + j - 1, 13).Value = tot_Profit * fee
                arProfit(p) = (open_price / Cells(i + j - 1, 5).Value - 1) * fee
                p = p + 1
            End If
            
        End If
        i = i + 1
        
    Loop Until i > end_row
    
    
    For i = 1 To trade_cnt
        Sheet1.Cells(20 + page, i + 16).Value = arProfit(i)
        
        'Debug.Print arProfit(i)
    Next i
    
    
    
        For i = 1 To trade_cnt
            ave = ave + arProfit(i)
        Next i
        Sheet1.Cells(20 + page, 5).Value = ave / trade_cnt
        
    Sheet1.Cells(20 + page, 4).Value = tot_Profit - 1
    'Debug.Print p, Worksheets(p).Name
    Sheet1.Cells(20 + page, 3).Value = Worksheets(page_num).Name
    Debug.Print Application.WorksheetFunction.average(Sheet1.Range(Cells(20 + page, 17), Cells(20 + page, trade_cnt)))
    
    Debug.Print page_num
       
    
End Sub

Sub tot()
    Worksheets(1).Activate
End Sub

Function My_R1C1(a, b, c, d)
    My_R1C1 = Range(Cells(a, b), Cells(c, d))
   ' Range(Cells(22, 17), Cells(22, 20)).Address(False, False)
End Function

