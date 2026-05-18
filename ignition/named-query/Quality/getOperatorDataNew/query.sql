-- Declare filters
DECLARE
	@lineID int = :line
,	@articleID int = :article
,	@startDate datetime2(0) = :startDate
,	@endDate datetime2(0) =  :endDate
,	@operator nvarchar(MAX) = :operator ;

WITH CTE_Main AS (
    SELECT
        stkprf_id
    ,   artikel
    ,   machine
    ,   min(testdatumtijd) datetime
    ,   max(bevinding) bevinding
    ,   min(tester) operatorName
    FROM [BMSPROD].[BMS-IGN].[dbo].[Inspections]
	WHERE bevinding > 0
    AND (tester =  @operator or  @operator = '-1')
    GROUP BY stkprf_id, artikel, machine
)
SELECT
    main.stkprf_id,
    Lines.LineID,
    Lines.Description as Line,
    Articles.ArticleID,
    Articles.ArticleNumber as Article,
    Articles.ArticleDescription,
    main.Datetime,
    convert(bit, iif(main.bevinding=1, 1, 0)) as Approved,
    main.OperatorName,
    -- create test results JSON
    JSON_QUERY(
        '{' + STRING_AGG(
            CONCAT(
                '"', STRING_ESCAPE(iif(tests.parameteromschrijving = 'Bedrukking',
               							'PrintOK',
               						iif(tests.parameteromschrijving = 'Visueel',
               							'VisualOK', tests.parameteromschrijving)), 'json'), '": ',
                '{',
                    '"Measured": ',       isnull(
                    								iif(tests.parametertype_txt = 'OK/NOK',
                    								convert(bit,iif(tests.bevinding = 1, 1, 0))
                    								,tests.gem_gemeten), -1000), ',',
                    '"ResultGood": ',     iif(tests.bevinding = 1, 1, 0), ',',
                    '"LowLimit": ',       ISNULL(tests.ondergrens, 0), ',',
                    '"Standard": ',       ISNULL(tests.norm, 0), ',',
                    '"HighLimit": ',      ISNULL(tests.bovengrens, 0),
                '}'
            ),
            ','
        ) + '}'
    ) AS Results

FROM CTE_Main main
JOIN [BMSPROD].[BMS-IGN].[dbo].[Inspections] tests
ON tests.stkprf_id = main.stkprf_id
--AND tests.parameteromschrijving = main.parameteromschrijving
INNER JOIN [NLSTWDYK_DB_PROD].[dbo].[Articles] Articles
ON main.artikel = convert(nvarchar(max), Articles.ArticleNumber)
INNER JOIN [NLSTWDYK_DB_PROD].[dbo].[Lines] Lines
ON main.machine = Lines.Description
WHERE main.bevinding > 0 -- only include test that have been completed
AND main.datetime between @startDate and @endDate
AND (Lines.lineID = @lineID or @lineID = -1)
AND (Articles.articleID = @articleID or @articleID = -1)

GROUP BY
    main.stkprf_id,
    main.datetime,
    main.bevinding,
    main.operatorName,
    Articles.ArticleID,
    Articles.ArticleNumber,
    Lines.Description,
    Lines.LineID,
    Articles.ArticleDescription

order by main.stkprf_id desc