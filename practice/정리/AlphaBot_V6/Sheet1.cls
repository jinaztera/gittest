VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "Sheet1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Sub 통계()
    UF_input.Show
End Sub



'Sub 난수()
'
'    Dim intNum As Variant
'    ReDim intNum(0 To 10)
'    For i = 0 To 10
'        intNum(i) = Int(Rnd * 145) + 2
''        Debug.Print "intNum" + Str(i) + "=" + Str(intNum(i))
'    Next i
'
'    '''어레이 출력
'
'    intNum = SortArray(intNum)
'    For Each element In intNum
'        Debug.Print element
'    Next
'    For i = 0 To 10
'    Debug.Print intNum(i)
'    Next i
'
'
'End Sub
'ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
'Function SortArray(intNum As Variant)
'
'Dim i As Long
'Dim j As Long
'Dim Temp
'
''Sort the Array A-Z
'For i = LBound(intNum) To UBound(intNum) - 1
'    For j = i + 1 To UBound(intNum)
'        If UCase(intNum(i)) > UCase(intNum(j)) Then
'            Temp = intNum(j)
'            intNum(j) = intNum(i)
'            intNum(i) = Temp
'        End If
'    Next j
'Next i
'
'SortArray = intNum
'
'End Function


