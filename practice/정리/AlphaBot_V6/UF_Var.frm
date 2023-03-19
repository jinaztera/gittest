VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} UF_Var 
   Caption         =   "UserForm1"
   ClientHeight    =   3015
   ClientLeft      =   120
   ClientTop       =   465
   ClientWidth     =   4560
   OleObjectBlob   =   "UF_Var.frx":0000
   StartUpPosition =   1  '소유자 가운데
End
Attribute VB_Name = "UF_Var"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Public fee As Double
Public ma1 As Integer
Public ma2 As Integer
Private Sub CB2_Click()
    ma1 = Me.TB_ma1.Value
    ma2 = Me.TB_ma2.Value
    fee = Me.TB_fee.Value / 100
    Range("G8").Value = ma1
    Range("G9").Value = ma2
    Range("G10").Value = fee


'    Range("G8").Value = Me.TB_ma1.Value
'    Range("G9").Value = Me.TB_ma2.Value
'    Range("G10").Value = Me.TB_fee.Value / 100
    
    Unload UF_Var
    
    Call Sheet1.난수
End Sub

Private Sub Label2_Click()

End Sub
