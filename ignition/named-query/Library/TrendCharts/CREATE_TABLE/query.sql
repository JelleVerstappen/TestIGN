CREATE TABLE [dbo].[TrendCharts](
[Active] [bit] NULL,
[TrendChartID] [int] IDENTITY(1,1) NOT NULL,
[TrendChartName] [nvarchar](max) NOT NULL,
[TrendChartConfig] [nvarchar](max) NULL,
[TrendChartIsPrivate] [bit] NULL,
[UserID] [int] NULL,
[Created] [datetime] NULL,
[CreatedBy] [int] NULL,
[Modified] [datetime] NULL,
[ModifiedBy] [int] NULL,
CONSTRAINT [PK_TrendCharts] PRIMARY KEY CLUSTERED
(
[TrendChartID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]