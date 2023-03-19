VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} UF_input 
   Caption         =   "투자전략"
   ClientHeight    =   5355
   ClientLeft      =   120
   ClientTop       =   465
   ClientWidth     =   4590
   OleObjectBlob   =   "UF_input.frx":0000
   StartUpPosition =   1  '소유자 가운데
End
Attribute VB_Name = "UF_input"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Option Explicit
Public Count As Integer


Private Sub CB1_Click()
    Debug.Print
    Debug.Print Me.TB_start.Value
    Sheet1.Range("C8") = Me.TB_start.Value
'    If Me.TB_end.Value = "" Then
    Sheet1.Range("C9") = Me.TB_period.Value
'        Sheet1.Range("C10") = DateSerial(Left(Me.TB_start.Value, 4), Mid(Me.TB_start.Value, 6, 2), Right(Me.TB_start.Value, 2)) + Me.TB_period.Value
        
'    ElseIf Me.TB_period.Value = "" Then
'        Sheet1.Range("C9") = Me.TB_start.Value - Me.TB_end.Value
    Sheet1.Range("C10") = Me.TB_end.Value
    Sheet1.Range("J8") = Me.TB_Count.Value
    Count = Me.TB_Count.Value
    
'    End If
    Unload UF_input
    UF_Var.Show

End Sub

Private Sub Label1_Click()

End Sub

Private Sub Label2_Click()

End Sub

Private Sub Label3_Click()

End Sub

Private Sub Label4_Click()

End Sub

Private Sub TB_start_Change()

End Sub
