/*
alter session set nls_date_format='Dd-MON-YY HH24:MI:SS';
set lines 250
set pages 2000
col name format a26
col username format a15
col program format a40
col SESS_CPU_SECS wra format 999,999,999.99
col LAST_CPU_SECS wra format 999,999,999.99
col logon_secs  wra format 999,999,999
col Percent  wra format 999.99
*/

SELECT * FROM
(
select sess_cpu.con_id,
       sess_cpu.sid,
       NVL(sess_cpu.username, 'Oracle Process') username,
       sess_cpu.status,
       sess_cpu.logon_time,
       round ((sysdate-sess_cpu.logon_time)*1440*60) logon_SECS,
       --call_cpu.value/100 CALL_CPU_SECS,
       sess_cpu.value/100 SESS_CPU_SECS,
       --round((sess_cpu.value/100)/round((sysdate - sess_cpu.logon_time)*1440*60)*100,2) Percent_call_cpu,
       --(sess_cpu.value - call_cpu.value)/100 LAST_CPU_SECS,
       nvl(sess_cpu.module, sess_cpu.program) module_info,
       sess_cpu.sql_id,
       (SELECT Min(sql_text) from V$SQL WHERE sql_id=sess_cpu.sql_id) sql_text
from
      (select se.con_id,
              se.sql_id,
              ss.statistic#,
              se.sid,
              se.username,
              se.status,
              se.program,
              se.logon_time,
              sn.name,
              ss.Value,
              se.MODULE
      from    v$session se,
              v$sesstat ss,
              v$statname sn
      WHERE   se.sid=ss.sid
        and   sn.statistic#=ss.statistic#
        and   sn.name in ('CPU used by this session')
      ) sess_cpu,

      (select se.con_id,
              ss.statistic#,
              se.sid,
              ss.value,
              value/100 seconds
       from   v$session se,
              v$sesstat ss,
              v$statname sn
       where  se.sid=ss.sid
         and  sn.statistic#=ss.statistic#
         and  sn.name in ('CPU used when call started')
      ) call_cpu

WHERE  sess_cpu.sid=call_cpu.sid
  AND  sess_cpu.con_id=call_cpu.con_id
)
--WHERE USERNAME <> 'Oracle Process'
ORDER BY sid