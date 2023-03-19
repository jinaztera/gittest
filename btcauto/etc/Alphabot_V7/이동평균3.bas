Attribute VB_Name = "이동평균3"
Option Explicit
Private start_row, end_row As Integer
Private page, page_count, page_num As Integer
Private MA(2) As Integer
Private long_cnt, short_cnt As Integer
Private arPage() As Variant

Sub start()
    Dim i As Integer
    page_count = Sheet1.Cells(8, 10).Value
'    ReDim arPage(1 To page_count)
    Debug.Print page, page_count

'    For i = 1 To page_count
'        arPage(i) = Int(Rnd * 145) + 1
'        Debug.Print "intNum" + Str(i) + "=" + Str(arPage(i))
'    Next i

    page = 0
    Call rotate

End Sub

Sub rotate()
    'Debug.Print "page", page

    If page <= page_count Then
        page = page + 1
        Call 찾기
    Else
        Call 종료
    End If
    

End Sub


Sub 찾기()
    Dim i, j, last As Integer
    'Worksheets(2).Activate
    page_num = Int(Rnd * 138) + 1
    Worksheets(page_num).Activate
    Dim start_date, end_date As Date
    last = Range("A10000").End(xlUp).Row
       
    Debug.Print page_num
       
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
                    Debug.Print end_date = Cells(j, 1)
                    Debug.Print end_row, Cells(j, 1).Row
                End If
            Next j
        End If
        
    Next i
pass:
    If start_row = 0 Or end_row = 0 Then
        page = page - 1
        Call rotate
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
            If Cells(i, 9).Value = 1 Then
                long_cnt = long_cnt + 1
                Cells(i + 1, 10).Value = "매수진입"
            ElseIf Cells(i, 9).Value = 2 Then
                Cells(i + 1, 10).Value = "매도진입"
                short_cnt = short_cnt + 1
            End If
            
        End If
    Next i
    
    If short_cnt = 0 Or long_cnt = 0 Then
        page = page - 1
        Call rotate
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
            
            If Cells(i + 1, 10).Value = "매도진입" Or i + 1 = end_row Then
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
            
            If Cells(i + 1, 10).Value = "매수진입" Or i + 1 = end_row Then
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
        Sheet1.Cells(20 + page, 4).Value = ave / trade_cnt
        
    Sheet1.Cells(20 + page, 3).Value = tot_Profit - 1
    'Debug.Print p, Worksheets(p).Name
    Sheet1.Cells(20 + page, 2).Value = Worksheets(page_num).Name
    
    
    
    If page < page_count Then
        Call rotate
    End If
    
    Call tot
End Sub

Sub tot()
    
    Worksheets(1).Activate
End Sub

Sub 종료()
    
    
End Sub

'Sub MA() '매수 매도 전략
'
'    Dim MA(2)    As Long
'    Dim r       As Range
'    Dim lngR    As Long
'    Dim a       As Long
'    Dim lngS    As Long
'    Dim lngProfit As Double
'    Dim lngBuy As Long
'    Dim lngSell As Long
'
'    Dim Str_start As String
'    Dim Str_end As String
'    Dim lngOpen As Double '진입가격
'    Dim lngClose As Double '청산가격
'    Dim lngMoney As Double
'
'    Dim Int_s As Integer
'    Dim Int_e As Integer
'    Dim last As Long
'
'    Dim Dou_Var() As Double
'
'    lngD(1) = InputBox(Prompt:="이동평균(1)")
'    lngD(2) = InputBox(Prompt:="이동평균(2)")
'
'    Worksheets("통계").Cells(6, 4).Value = lngD(1)
'    Worksheets("통계").Cells(7, 4).Value = MA(2)
'
'    Str_start = Worksheets("통계").Cells(6, 7).Value
'    Str_end = Worksheets("통계").Cells(7, 7).Value
'
'    For q = 2 To Worksheets.Count
'        Worksheets(q).Activate
'        '초기 설정
'
'        Int_s = 0
'        Int_e = 0
'        last = Range("A10000").End(xlUp).Row
'        Worksheets(q).Activate
'        '초기 설정
'
'        If Str_start < Cells(2, 1).Value Then
'            Str_start = Cells(2, 1).Value
'
'        ElseIf Str_start > Cells(last, 1).Value Then
'            GoTo last:
'
'
'        Else
'            Do
'                Int_s = Int_s + 1
'                Debug.Print Int_s
'
'            Loop Until Str_start = Cells(Int_s, 1)
'        End If
'
'        last = Range("A10000").End(xlUp).Row
'
'        If Str_end > Cells(last, 1) Then
'            Str_end = Cells(last, 1).Value
'
'        Else
'            Do
'                 Int_e = Int_e + 1
'                Debug.Print Int_e
'
'            Loop Until Str_end = Cells(Int_e, 1).Value
'        End If
'
'
'
'        lngMoney = 1
'        lngBuy = 0
'        lngSell = 0
'
'
'        lngR = Range("A10000").End(xlUp).Row
'
'        Range("F2:O" & lngR).Clear
'
'
'        For j = 1 To 2
'            For i = 1 To lngR
'                If Range("E" & i + MA(j)).Value = "" Then
'                    Exit For
'                End If
'
'                Set r = Range("E" & i + 1 & ":E" & i + MA(j))
'                Cells(i + MA(j), j + 5).Value = Application.Sum(r) / r.Cells.Count
'            Next i
'        Next j
'
'        '매수 매도 전략
'
'        a = 2
'        Do
'            If Cells(a, 6).Value = 0 Or Cells(a, 7).Value = 0 Then
'                Cells(a, 8).Value = ""
'            ElseIf Cells(a, 6).Value > Cells(a, 7).Value Then
'                Cells(a, 8).Value = 1
'            Else
'                Cells(a, 8).Value = 2
'            End If
'
'            a = a + 1
'        Loop Until a = lngR + 1
'
'        lngS = Range("H1").End(xlDown).Row '거래 시작
'
'        '손이익
'
'        lngProfit = 0
'        Debug.Print Int_s
'
'        Do
'            If Cells(Int_s, 8).Value = 1 Then
'                lngOpen = Cells(Int_s + 1, 2).Value
'                lngBuy = lngBuy + 1
'                Cells(Int_s + 1, 9).Value = "매수진입"
'                Cells(Int_s + 1, 10).Value = Cells(Int_s + 1, 2).Value '진입가
'                Cells(Int_s + 1, 11).Value = Cells(Int_s + 1, 5).Value - Cells(Int_s + 1, 2).Value '당일손이익
'                lngProfit = lngProfit + Cells(Int_s + 1, 5).Value - Cells(Int_s + 1, 2).Value '누적손이익
'                Cells(Int_s + 1, 12).Value = lngProfit '누적손이익
'
'                If Cells(Int_s + 2, 8).Value = "" Then
'                    lngClose = Cells(Int_s + 1, 5).Value
'                    Cells(Int_s + 1, 13).Value = lngClose - lngOpen
'                    If lngOpen = 0 Then
'                        GoTo last:
'                    End If
'                    Cells(Int_s + 1, 14).Value = (lngClose / lngOpen - 1) * 100
'                    lngMoney = lngMoney * (lngClose / lngOpen)
'                    Cells(Int_s + 1, 15).Value = lngMoney
'
'                ElseIf Cells(Int_s + 1, 8).Value = 1 Then
'                    Do
'                        Cells(Int_s + 2, 11).Value = Cells(Int_s + 2, 5).Value - Cells(Int_s + 1, 5).Value
'                        lngProfit = lngProfit + Cells(Int_s + 2, 5).Value - Cells(Int_s + 1, 5).Value
'                        Cells(Int_s + 2, 12).Value = lngProfit
'                        Int_s = Int_s + 1
'                        Debug.Print Int_s
'                    Loop Until Cells(Int_s + 1, 8) = 2 Or Cells(Int_s + 2, 8).Value = ""
'                    Cells(Int_s + 1, 9).Value = "청산"
'                    lngClose = Cells(Int_s + 1, 5).Value
'                    Cells(Int_s + 1, 10).Value = lngClose
'                    Cells(Int_s + 1, 13).Value = lngClose - lngOpen
'                    Cells(Int_s + 1, 14).Value = (lngClose / lngOpen - 1) * 100
'                    lngMoney = lngMoney * (lngClose / lngOpen)
'                    Cells(Int_s + 1, 15).Value = lngMoney
'
'                 ElseIf Cells(Int_s + 1, 8).Value = 2 Then
'                    lngClose = Cells(Int_s + 1, 5).Value
'                    Cells(Int_s + 1, 13).Value = lngClose - lngOpen
'                    Cells(Int_s + 1, 14).Value = (lngClose / lngOpen - 1) * 100
'                    lngMoney = lngMoney * (lngClose / lngOpen)
'                    Cells(Int_s + 1, 15).Value = lngMoney
'
'                End If
'
'            ElseIf Cells(Int_s, 8).Value = 2 Then
'                lngOpen = Cells(Int_s + 1, 2).Value
'                lngSell = lngSell + 1
'                Cells(Int_s + 1, 9).Value = "매도진입"
'                Cells(Int_s + 1, 10).Value = Cells(Int_s + 1, 2).Value '진입가
'                Cells(Int_s + 1, 11).Value = Cells(Int_s + 1, 2).Value - Cells(Int_s + 1, 5).Value  '손이익
'                lngProfit = lngProfit + Cells(Int_s + 1, 2).Value - Cells(Int_s + 1, 5).Value '누적 손이익
'                Cells(Int_s + 1, 12).Value = lngProfit
'
'                If Cells(Int_s + 2, 8).Value = "" Then
'                    lngClose = Cells(Int_s + 1, 5).Value
'                    Cells(Int_s + 1, 13).Value = lngOpen - lngClose
'                    If lngClose = 0 Then
'                        GoTo last:
'                    End If
'                    Cells(Int_s + 1, 14).Value = (lngOpen / lngClose - 1) * 100
'                    lngMoney = lngMoney * (lngOpen / lngClose)
'                    Cells(Int_s + 1, 15).Value = lngMoney
'
'                ElseIf Cells(Int_s + 1, 8).Value = 2 Then
'                    Do
'                        Cells(Int_s + 2, 11).Value = Cells(Int_s + 1, 5).Value - Cells(Int_s + 2, 5).Value
'                        lngProfit = lngProfit + Cells(Int_s + 1, 5).Value - Cells(Int_s + 2, 5).Value
'                        Cells(Int_s + 2, 12).Value = lngProfit
'                        Int_s = Int_s + 1
'                        Debug.Print Int_s
'                    Loop Until Cells(Int_s + 1, 8) = 1 Or Cells(Int_s + 2, 8).Value = ""
'
'                    Cells(Int_s + 1, 9).Value = "청산"
'                    lngClose = Cells(Int_s + 1, 5).Value
'                    Cells(Int_s + 1, 10).Value = lngClose
'                    Cells(Int_s + 1, 13).Value = lngOpen - lngClose
'                    Cells(Int_s + 1, 14).Value = (lngOpen / lngClose - 1) * 100
'                    lngMoney = lngMoney * (lngOpen / lngClose)
'                    Cells(Int_s + 1, 15).Value = lngMoney
'
'                ElseIf Cells(Int_s + 1, 8).Value = 1 Then
'                    lngClose = Cells(Int_s + 1, 5).Value
'                    Cells(Int_s + 1, 13).Value = lngOpen - lngClose
'                    Cells(Int_s + 1, 14).Value = (lngOpen / lngClose - 1) * 100
'                    lngMoney = lngMoney * (lngOpen / lngClose)
'                    Cells(Int_s + 1, 15).Value = lngMoney
'
'                End If
'
'            End If
'
'            Debug.Print lngBuy
'            Debug.Print lngSell
'            Int_s = Int_s + 1
'
'        Loop Until Int_s > Int_e
'        '통계
'
'last:
'
'        Worksheets("통계").Cells(10, q + 1).Value = Int_s - 1 '거래일수
'        Worksheets("통계").Cells(11, q + 1).Value = Str_start '시작일
'        Worksheets("통계").Cells(12, q + 1).Value = Cells(Int_e, 1) '종료일
'        Worksheets("통계").Cells(13, q + 1).Value = lngMoney - 1 '누적수익률
'        Worksheets("통계").Cells(16, q + 1).Value = lngBuy + lngSell '거래횟수
'        Worksheets("통계").Cells(17, q + 1).Value = lngBuy '매수횟수
'        Worksheets("통계").Cells(18, q + 1).Value = lngSell '매도횟수
'        Worksheets("통계").Cells(19, q + 1).Value = (Int_s - 1) / (lngBuy + lngSell)   '평균거래일수
'
'
'    Next q
'
'    Worksheets(1).Activate
'
'End Sub



