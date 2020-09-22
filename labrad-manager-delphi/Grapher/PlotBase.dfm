object PlotBaseForm: TPlotBaseForm
  Left = 192
  Top = 255
  Width = 811
  Height = 482
  Caption = 'PlotBaseForm'
  Color = clBtnFace
  DragMode = dmAutomatic
  Font.Charset = ANSI_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  Icon.Data = {
    0000010001001010000001000800680500001600000028000000100000002000
    000001000800000000000000000000000000000000000000000000000000110D
    FD001F1CF900E0570000E0570300E05803002825F9002824FF00392AEB00BC53
    43004935E100AB632800AC642800AD6428003633F600DE651700AE652800AE65
    2900AF662900AF662A00B0662A003A37F700B1682A00B2682A00B3682B003E38
    F500B4692B00B66A2D00B76B2D00B96D2E00BB6E2F004340F400BD6F3000BE71
    3000B0636900C0723200C2733200C3733300DE742700C4743400C5753400397E
    4600C67634005650EE0044844D005452F1005552F2005553F000E0823000DF81
    3800DF833C003D8F4B00DF883E0047925100DF884000605EFA00DE894000615E
    FC003C984A006664F1006968F200E78D52006A68FC006E6CF0003DA34C004AA2
    58007573F1007573F4004FA65E007976F400EAA06C008280FD00E8A56B00EDA4
    720060B56C007FAC870063B66F008B89F90069B57400EAA77800EEA87B007CB4
    8500B89DCA0077BB8100EEAD880084B88B0086B98F009A98F900EEB18B00EEB4
    8300E8B78B00EDB88E00A8BBA700A5A4F60091C399008DC79300ACABFD00A8C7
    AD00B1B0FF00F4C5AA00EFC8A400E8CBB200BCD0BF00C9C4E600C9CFC400C1C1
    F900C3D5C600B3DBB800BADFBF00F3DCC800C5E1CA00D3D2FC00DED8E600F8E7
    D700E9E6E400EAE6E400E1E1FD00F0EAE500E6E6FD00E6E6FE00E8E7FD00E8E8
    FE00E8F0EA00EAF1EB00F4F8F500F5F9F600F7F9F700F8FAF800FDFAF800FEFD
    FC00FFFFFF000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000008181
    81818181818181818181818181818119171615131211100F0C0C0B0A0A81811A
    6569677D817281817181795B7B81811B7A4A2B2860818181817E34548181811C
    6681815532507C81815D39818181811D5F7881816D4043524D3F6A817681811F
    6106818181535E4B496B8181388181206F00464F020403628181818105818122
    813D010848803C0E57818136148181238181070981818145254E730D51818124
    745821184C8181815A30313533818126802F47561E6E8181752C2A6381818127
    70377F81442D423B2E3A77818181812964598181815C3E416881818181818129
    6C81818181818181818181818181818181818181818181818181818181810000
    0000000000000000000000000000000000000000000000000000000000000000
    000000000000000000000000000000000000000000000000000000000000}
  Menu = MainMenu1
  OldCreateOrder = False
  OnClose = FormClose
  OnCloseQuery = FormCloseQuery
  OnDragOver = FormDragOver
  OnResize = FormResize
  PixelsPerInch = 96
  TextHeight = 13
  object Splitter1: TSplitter
    Left = 1
    Top = 0
    Width = 4
    Height = 409
  end
  object Panel1: TPanel
    Left = 0
    Top = 0
    Width = 1
    Height = 409
    Align = alLeft
    BevelOuter = bvNone
    BiDiMode = bdLeftToRight
    ParentBiDiMode = False
    TabOrder = 0
    object Splitter2: TSplitter
      Left = 0
      Top = 365
      Width = 1
      Height = 3
      Cursor = crVSplit
      Align = alBottom
    end
    object Panel2: TPanel
      Left = 0
      Top = 0
      Width = 1
      Height = 365
      Align = alClient
      BevelOuter = bvNone
      BorderStyle = bsSingle
      Constraints.MinHeight = 75
      TabOrder = 0
      object Panel4: TPanel
        Left = 0
        Top = 0
        Width = 1
        Height = 21
        Align = alTop
        Caption = 'Chat'
        Color = clActiveCaption
        Font.Charset = DEFAULT_CHARSET
        Font.Color = clCaptionText
        Font.Height = -11
        Font.Name = 'MS Sans Serif'
        Font.Style = [fsBold]
        ParentFont = False
        TabOrder = 0
      end
      object Memo1: TMemo
        Left = 0
        Top = 21
        Width = 1
        Height = 344
        Align = alClient
        BorderStyle = bsNone
        ReadOnly = True
        ScrollBars = ssVertical
        TabOrder = 1
      end
    end
    object Panel3: TPanel
      Left = 0
      Top = 368
      Width = 1
      Height = 41
      Align = alBottom
      BevelOuter = bvNone
      BorderStyle = bsSingle
      Constraints.MinHeight = 25
      TabOrder = 1
      object Memo2: TMemo
        Left = 0
        Top = 0
        Width = 1
        Height = 41
        Align = alClient
        BorderStyle = bsNone
        PopupMenu = PopupMenu1
        TabOrder = 0
      end
    end
  end
  object Panel5: TPanel
    Left = 5
    Top = 0
    Width = 771
    Height = 409
    Align = alClient
    BevelOuter = bvNone
    BorderStyle = bsSingle
    Color = clWindow
    TabOrder = 1
    OnResize = FormResize
    object Image1: TImage
      Left = 0
      Top = 0
      Width = 767
      Height = 405
      Align = alClient
      OnMouseDown = Image1MouseDown
      OnMouseMove = Image1MouseMove
      OnMouseUp = Image1MouseUp
    end
    object Shape1: TShape
      Left = 76
      Top = 64
      Width = 173
      Height = 109
      Brush.Style = bsClear
      Pen.Color = clRed
      Pen.Style = psDot
      Visible = False
    end
  end
  object StatusBar1: TStatusBar
    Left = 0
    Top = 409
    Width = 803
    Height = 19
    Panels = <>
    SimplePanel = True
  end
  object Panel6: TPanel
    Left = 776
    Top = 0
    Width = 27
    Height = 409
    Align = alRight
    BevelOuter = bvNone
    TabOrder = 3
    object CloneButton: TSpeedButton
      Left = 2
      Top = 2
      Width = 25
      Height = 25
      AllowAllUp = True
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        04000000000000010000130B0000130B00001000000000000000000000000000
        800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF0033333333B333
        333B33FF33337F3333F73BB3777BB7777BB3377FFFF77FFFF77333B000000000
        0B3333777777777777333330FFFFFFFF07333337F33333337F333330FFFFFFFF
        07333337F33333337F333330FFFFFFFF07333337F33333337F333330FFFFFFFF
        07333FF7F33333337FFFBBB0FFFFFFFF0BB37777F3333333777F3BB0FFFFFFFF
        0BBB3777F3333FFF77773330FFFF000003333337F333777773333330FFFF0FF0
        33333337F3337F37F3333330FFFF0F0B33333337F3337F77FF333330FFFF003B
        B3333337FFFF77377FF333B000000333BB33337777777F3377FF3BB3333BB333
        3BB33773333773333773B333333B3333333B7333333733333337}
      NumGlyphs = 2
      OnClick = CloneButtonClick
    end
    object SpeedButton1: TSpeedButton
      Left = 2
      Top = 34
      Width = 25
      Height = 25
      Hint = 'Zoom'
      GroupIndex = 2
      Down = True
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        0400000000000001000000000000000000001000000000000000000000000000
        8000008000000080800080000000800080008080000080808000C0C0C0000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00888888888888
        888888888888888888FF8888888888888448888888888888877F888888888888
        4CC88888888888887778888888888884CC88888888888887778888888888884C
        C88888888FFF88777888888700078BCC8888888F7778F77788888806888600B8
        88888877888777788888808EEEEE8088888887F8888887F8888876EEE66EE678
        888887888888878F888808EEEEE6E80888887F888888887F888808EFEEE6E808
        88887F888888887F888808EFEEEEE808888878F88888887F888876EEFFEEE678
        888887F8888887F88888808EEEEE80888888878FF888F7888888880688860888
        888888778FF77888888888870007888888888888777888888888}
      NumGlyphs = 2
      ParentShowHint = False
      ShowHint = True
    end
    object SpeedButton2: TSpeedButton
      Left = 2
      Top = 60
      Width = 25
      Height = 25
      Hint = 'Pan'
      GroupIndex = 2
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        0400000000000001000000000000000000001000000000000000000000000000
        8000008000000080800080000000800080008080000080808000C0C0C0000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00555555555555
        55555555555555FFF555555555555000555555555555F7775F55555555550000
        05555555555F75F575F555555550E000005555555557575F57F55555550EEE00
        005555555F75F575F7F555550000EEE00055555F77775F5757555550FBFB0EEE
        055555F7555575F57555550FBFBFB0E055555F7555555757555550FBFBFBFB05
        5555575FF555557F555550B0BFBFBF05555557F75FF5FF7F5555550BF0FB0B05
        55555575F75F757F555550BF0FB0BF05555557FF75F75F75555550F0FB0BF055
        555557575F75F7555555550FB05005555555557FF75775555555550B05555555
        5555557575555555555555505555555555555557555555555555}
      NumGlyphs = 2
      ParentShowHint = False
      ShowHint = True
    end
  end
  object PopupMenu1: TPopupMenu
    Left = 108
    Top = 1
    object Clear1: TMenuItem
      Caption = '&Clear'
      ShortCut = 16392
      OnClick = Clear1Click
    end
    object Send1: TMenuItem
      Caption = '&Send'
      ShortCut = 16397
      OnClick = Send1Click
    end
  end
  object Timer1: TTimer
    Enabled = False
    Interval = 50
    OnTimer = Timer1Timer
    Left = 12
    Top = 4
  end
  object MainMenu1: TMainMenu
    Left = 76
    Top = 4
    object MenuFile: TMenuItem
      Caption = '&File'
      object MenuFSaveData: TMenuItem
        Caption = '&Save Data...'
        Enabled = False
        ShortCut = 16467
      end
      object MenuFSaveImage: TMenuItem
        Caption = 'Save &Image...'
        Enabled = False
        ShortCut = 16457
      end
      object N2: TMenuItem
        Caption = '-'
      end
      object MenuFPrint: TMenuItem
        Caption = '&Print...'
        Enabled = False
        ShortCut = 16464
      end
      object N1: TMenuItem
        Caption = '-'
      end
      object MenuFClose: TMenuItem
        Caption = '&Close'
        ShortCut = 16411
        OnClick = MenuFCloseClick
      end
    end
    object MenuEdit: TMenuItem
      Caption = '&Edit'
      object MenuECopyData: TMenuItem
        Caption = '&Copy Data...'
        Enabled = False
        ShortCut = 16451
      end
    end
    object MenuView: TMenuItem
      Caption = '&View'
    end
  end
  object Timer2: TTimer
    Enabled = False
    Interval = 500
    OnTimer = Timer1Timer
    Left = 44
    Top = 4
  end
end
