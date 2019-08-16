PROMPT CREATE OR REPLACE FUNCTION export_apex_application
CREATE OR REPLACE FUNCTION export_apex_application(P_APP_ID VARCHAR2) RETURN CLOB IS
/*
  Creata da...: Marco Valaguzza
  Data........: 04/12/2018
  Descrizione.: Ricevuto in input l'id di un'applicazione Oracle Application Express,
                restituisce un clob contentente tutti i dati in forma testuale che la
                compongono.
                Attenzione! Siccome tale funzione è nata per essere usata dal programma SmiGrep,
                esterno ad Oracle, per problemi di conversioni di caratteri, si è forzato che il
                testo restituito da questa funzione, sia tutto in formato ASCII.

  Parametri INPUT: P_APP_ID = Identificativo dell'app. Presente nella tabella APEX_APPLICATIONS
            OUTPUT: clob in formato ASCII
*/
  L_CLOB          CLOB;
  L_LINES         HTP.HTBUF_ARR;
  L_NUM           NUMBER:=999999;
  l_workspace_id  NUMBER;
BEGIN
  -- Inizializzazioni di libreria
  OWA.NUM_CGI_VARS    := 0;
  OWA.CGI_VAR_NAME(1) := 1;
  OWA.CGI_VAR_VAL(1)  := 1;
  OWA.INIT_CGI_ENV(1, OWA.CGI_VAR_NAME, OWA.CGI_VAR_VAL);

  -- Inizializzo il clob
  DBMS_LOB.CREATETEMPORARY(L_CLOB, TRUE);

  -- Ricerco il workspace dell'applicazione richiesta
  SELECT WORKSPACE_ID
  INTO   l_workspace_id
  FROM   APEX_APPLICATIONS
  WHERE  WORKSPACE = 'SMILE'
    AND  APPLICATION_ID = p_app_id;

  -- Richiamo la funzione che esporta il contenuto di un'applicazione Apex
  APEX_UTIL.EXPORT_APPLICATION (P_WORKSPACE_ID => L_WORKSPACE_ID,
                                P_APPLICATION_ID => p_app_id);

  -- Prendo la pagina e la carico nel clob. La variabile L_NUM restituisce il numero di righe contenute nella pagina.
  OWA.GET_PAGE(L_LINES, L_NUM);
  Dbms_Output.Put_Line('numero riga' || l_num);
  FOR I IN 1..L_NUM LOOP
     --IF i = 13618 THEN
     --   Dbms_Output.Put_Line(L_LINES(I));
         --Dbms_Output.Put_Line(convert(L_LINES(I),'US7ASCII'));
     --END IF;
     -- Siccome Python aveva problemi a prendere tutti i caratteri UTF8, si è deciso di convertire tutto in formato ASCII
     DBMS_LOB.APPEND(l_clob, convert(L_LINES(I),'US7ASCII'));
  END LOOP;

  -- Restituisco il clob
  RETURN l_clob;

/*
------------------------------------
-- Quanto segue è un piccolo test --
------------------------------------
declare
  v_clob CLOB;
begin
  v_clob := export_apex_application(153);
end;
*/

END;
/

