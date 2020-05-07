DECLARE
  v_fname_co UT_REPOR.FNAME_CO%TYPE := 'MARCO';
  v_page_nu  UT_REPOR.PAGE_NU%TYPE  := 1;

PROCEDURE CARICA(p_fname_co UT_REPOR.FNAME_CO%TYPE,
                 p_page_nu  UT_REPOR.PAGE_NU%TYPE,
                 p_pos NUMBER) IS
BEGIN
  FOR R IN (select se.con_id,
                   se.sid,
                   username,
                   status,
                   logon_time,
                   round ((sysdate-logon_time)*1440*60) logon_SECS,
                   value/100 SESS_CPU_SECS,
                   nvl(se.module, se.program) module_info,
                   se.sql_id,
                   (SELECT Min(sql_text) from V$SQL WHERE sql_id=se.sql_id) sql_text
            from   v$session se,
                   v$sesstat ss,
                   v$statname sn
            WHERE  username IS NOT NULL
              AND  se.sid=ss.sid
              and  sn.statistic#=ss.statistic#
              and  sn.name in ('CPU used by this session')
           ) LOOP

      UT_REPORT.CREATE_UT_REPOR(p_fname_co,
                                p_page_nu,
                                'MVALAGUZ',
                                SYSDATE,
                                p_pos,     --CAMPO1
                                r.SID,     --CAMPO2
                                r.USERNAME,  --CAMPO3
                                r.STATUS,    --CAMPO4
                                r.LOGON_TIME, --CAMPO5
                                r.LOGON_SECS,  --CAMPO6
                                r.SESS_CPU_SECS, --CAMPO7
                                r.MODULE_INFO, --CAMPO8
                                r.SQL_ID, --CAMPO9
                                SubStr(r.SQL_TEXT,1,1000)); --CAMPO10
  END LOOP;
END;

PROCEDURE DIFFERENZE(p_fname_co   UT_REPOR.FNAME_CO%TYPE,
                     p_page_nu    UT_REPOR.PAGE_NU%TYPE,
                     p_pos_fine   NUMBER,
                     p_pos_inizio NUMBER) IS
  rec_ut_repor UT_REPOR%ROWTYPE;
  v_diffe      NUMBER;
  v_totale     NUMBER:=0;
BEGIN
  FOR r IN (SELECT *
            FROM   UT_REPOR
            WHERE  FNAME_CO=p_fname_co
              AND  PAGE_NU =p_page_nu
              AND  CAMPO1  =p_pos_fine) LOOP
      BEGIN
        -- ricerco record corrispondente in sessione precedente
        SELECT *
        INTO   rec_ut_repor
        FROM   UT_REPOR
        WHERE  FNAME_CO=p_fname_co
          AND  PAGE_NU =p_page_nu
          AND  CAMPO1  =p_pos_inizio
          AND  CAMPO2  =R.CAMPO2;

        -- calcolo differenza
        v_diffe  := R.CAMPO7 - rec_ut_repor.CAMPO7;
        v_totale := v_totale + Nvl(v_diffe,0);

        -- eseguo la differenza tra tempo attuale e tempo precedente
        UPDATE UT_REPOR
        SET    CAMPO21 = v_diffe
        WHERE  FNAME_CO= R.FNAME_CO
           AND PAGE_NU = R.PAGE_NU
           AND POSIZ_NU= R.POSIZ_NU;
      EXCEPTION
        WHEN No_Data_Found THEN
             NULL;
      END;
  END LOOP;

  -- calcolo le percentuali
  UPDATE UT_REPOR
  SET    CAMPO22 = CAMPO21 * 100 / v_totale
  WHERE  FNAME_CO= p_fname_co
     AND PAGE_NU = p_page_nu
     AND CAMPO1  = p_pos_fine;
END;

BEGIN
  SMILE.UT_REPORT.DELETE_UT_REPOR(v_fname_co, v_page_nu);

  -- CARICO SITUAZIONE INIZIALE
  CARICA(v_fname_co, v_page_nu, 1);

  -- ATTENDO 15 SECONDI
  DBMS_LOCK.SLEEP(15);

  -- CARICO NUOVA SITUAZIONE
  CARICA(v_fname_co, v_page_nu, 2);

  -- CALCOLO LE DIFFERENZE TRA DUE PAGINE
  DIFFERENZE(v_fname_co, v_page_nu, 2, 1);
END;

/

SELECT campo1 pos,
       campo2 sid,
       campo3 USERNAME,
       campo4 STATUS,
       campo5 LOGON_TIME,
       campo6 LOGON_SECS,
       campo7 SESS_CPU_SECS,
       campo8 MODULE_INFO,
       campo9 SQL_ID,
       campo10 SQL_TEXT,
       campo21 DIFFERENZA,
       campo22 PERCENTUALE
FROM ut_repor
WHERE fname_co='MARCO'
  AND PAGE_NU=1
  AND CAMPO1=2
ORDER BY CAMPO22 DESC, campo1, posiz_nu;