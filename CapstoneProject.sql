USE [CapstoneProject]
GO
/****** Object:  Table [dbo].[Security]    Script Date: 7/16/2022 12:13:43 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Security](
	[SecurityCode] [nvarchar](10) NOT NULL,
	[Description] [nvarchar](100) NULL,
 CONSTRAINT [PK_Symbol] PRIMARY KEY CLUSTERED 
(
	[SecurityCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Strategy]    Script Date: 7/16/2022 12:13:43 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Strategy](
	[StrategyId] [nvarchar](60) NOT NULL,
	[StrategyName] [nvarchar](100) NOT NULL,
	[TimeFrame] [nvarchar](400) NULL,
	[Frequency] [nchar](20) NULL,
	[StartDate] [datetime] NULL,
	[EndDate] [datetime] NULL,
 CONSTRAINT [PK_Strategy] PRIMARY KEY CLUSTERED 
(
	[StrategyId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[StrategyResult]    Script Date: 7/16/2022 12:13:43 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[StrategyResult](
	[StrategyResultId] [int] IDENTITY(1,1) NOT NULL,
	[SecurityCode] [nvarchar](10) NOT NULL,
	[StrategyId] [nvarchar](60) NOT NULL,
	[PortfolioProfitRate] [float] NULL,
	[PnL] [float] NULL,
	[MaxDrawdown] [float] NULL,
	[SharpeRatio] [float] NULL,
	[StrikeRate] [float] NULL,
	[NumberOfTrade] [int] NULL,
 CONSTRAINT [PK_StrategyResult] PRIMARY KEY CLUSTERED 
(
	[StrategyResultId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'ILF', N'iShares Latin America 40 ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'IYR', N'Shares U.S. Real Estate ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'IYZ', N'iShares U.S. Telecommunications ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'SPY', N'SPDR S&P 500 ETF Trust')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'VB', N'Vanguard Small-Cap ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'VBK', N'Vanguard Small-Cap Growth ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'VBR', N'Vanguard Small-Cap Value ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'VEA', N'Vanguard FTSE Developed Markets ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'VGK', N'Vanguard FTSE Europe ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'VO', N'Vanguard Mid-Cap ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'VOE', N'Vanguard Mid-Cap Value ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'VOT', N'Vanguard Mid-Cap Growth ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'VPL', N'Vanguard FTSE Pacific ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'VTV', N'Vanguard Value ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'VUG', N'Vanguard Growth ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'VV', N'Vanguard Large-Cap ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'VWO', N'Vanguard FTSE Emerging Markets ETF')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'XLB', N'Materials Select Sector SPDR Fund')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'XLE', N'Energy Select Sector SPDR Fund')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'XLF', N'Financial Select Sector SPDR Fund')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'XLI', N'Industrial Select Sector SPDR Fund')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'XLK', N'Technology Select Sector SPDR Fund')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'XLP', N'Consumer Staples Select Sector SPDR Fund')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'XLU', N'Utilities Select Sector SPDR Fund')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'XLV', N'Health Care Select Sector SPDR Fund')
GO
INSERT [dbo].[Security] ([SecurityCode], [Description]) VALUES (N'XLY', N'Consumer Discretionary Select Sector SPDR Fund')
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_During_GFC_1_Day_Position_Resizing', N'RSI with Position Resizing', N'During GFC(01 Jan 2006 - 31 Dec 2009)', N'daily               ', CAST(N'2006-01-01T00:00:00.000' AS DateTime), CAST(N'2009-12-31T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_During_GFC_1_Day_Static_Stop_Loss', N'RSI with Static Stop Loss', N'During GFC(01 Jan 2006 - 31 Dec 2009)', N'daily               ', CAST(N'2006-01-01T00:00:00.000' AS DateTime), CAST(N'2009-12-31T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_During_GFC_1_Day_Time_Based_Stop_Loss', N'RSI with Time Based Stop', N'During GFC(01 Jan 2006 - 31 Dec 2009)', N'daily               ', CAST(N'2006-01-01T00:00:00.000' AS DateTime), CAST(N'2009-12-31T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_During_GFC_1_Day_Vol_Adjusted_Stop_Loss', N'RSI with Volatility Adjusted Stop Loss', N'During GFC(01 Jan 2006 - 31 Dec 2009)', N'daily               ', CAST(N'2006-01-01T00:00:00.000' AS DateTime), CAST(N'2009-12-31T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_During_GFC_1_Day_wo_Risk_Management', N'RSI wo Risk Management', N'During GFC(01 Jan 2006 - 31 Dec 2009)', N'daily               ', CAST(N'2006-01-01T00:00:00.000' AS DateTime), CAST(N'2009-12-31T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_During_Pandemic_1_Day_Position_Resizing', N'RSI with Position Resizing', N'During Pandemic(01 Jan 2019 - 13 Jul 2022)', N'daily               ', CAST(N'2019-01-01T00:00:00.000' AS DateTime), CAST(N'2022-07-03T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_During_Pandemic_1_Day_Static_Stop_Loss', N'RSI with Static Stop Loss', N'During Pandemic(01 Jan 2019 - 13 Jul 2022)', N'daily               ', CAST(N'2019-01-01T00:00:00.000' AS DateTime), CAST(N'2022-07-03T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_During_Pandemic_1_Day_Time_Based_Stop_Loss', N'RSI with Time Based Stop', N'During Pandemic(01 Jan 2019 - 13 Jul 2022)', N'daily               ', CAST(N'2019-01-01T00:00:00.000' AS DateTime), CAST(N'2022-07-03T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_During_Pandemic_1_Day_Vol_Adjusted_Stop_Loss', N'RSI with Volatility Adjusted Stop Loss', N'During Pandemic(01 Jan 2019 - 13 Jul 2022)', N'daily               ', CAST(N'2019-01-01T00:00:00.000' AS DateTime), CAST(N'2022-07-03T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_During_Pandemic_1_Day_wo_Risk_Management', N'RSI wo Risk Management', N'During Pandemic(01 Jan 2019 - 13 Jul 2022)', N'daily               ', CAST(N'2019-01-01T00:00:00.000' AS DateTime), CAST(N'2022-07-03T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_Less_Volatie_1_Day_Position_Resizing', N'RSI with Position Resizing', N'Less Volatile(01 Jan 2014 - 31 Dec 2017)', N'daily               ', CAST(N'2014-01-01T00:00:00.000' AS DateTime), CAST(N'2017-12-31T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_Less_Volatile_1_Day_Static_Stop_Loss', N'RSI with Static Stop Loss', N'Less Volatile(01 Jan 2014 - 31 Dec 2017)', N'daily               ', CAST(N'2014-01-01T00:00:00.000' AS DateTime), CAST(N'2017-12-31T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_Less_Volatile_1_Day_Time_Based_Stop_Loss', N'RSI with Time Based Stop', N'Less Volatile(01 Jan 2014 - 31 Dec 2017)', N'daily               ', CAST(N'2014-01-01T00:00:00.000' AS DateTime), CAST(N'2017-12-31T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_Less_Volatile_1_Day_Vol_Adjusted_Stop_Loss', N'RSI with Volatility Adjusted Stop Loss', N'Less Volatile(01 Jan 2014 - 31 Dec 2017)', N'daily               ', CAST(N'2014-01-01T00:00:00.000' AS DateTime), CAST(N'2017-12-31T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[Strategy] ([StrategyId], [StrategyName], [TimeFrame], [Frequency], [StartDate], [EndDate]) VALUES (N'RSI_Less_Volatile_1_Day_wo_Risk_Management', N'RSI wo Risk Management', N'Less Volatile(01 Jan 2014 - 31 Dec 2017)', N'daily               ', CAST(N'2014-01-01T00:00:00.000' AS DateTime), CAST(N'2017-12-31T00:00:00.000' AS DateTime))
GO
ALTER TABLE [dbo].[StrategyResult]  WITH CHECK ADD  CONSTRAINT [FK_StrategyResult_Strategy] FOREIGN KEY([StrategyId])
REFERENCES [dbo].[Strategy] ([StrategyId])
GO
ALTER TABLE [dbo].[StrategyResult] CHECK CONSTRAINT [FK_StrategyResult_Strategy]
GO
