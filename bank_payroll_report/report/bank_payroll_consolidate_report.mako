<html>
<head>
    <style type="text/css">
        ${css}
        
        .normal_table1 {
			border:none;
			border-collapse: collapse;
		}

		.normal_table1 td {
			border-left: 1px solid #000;
			border-right: 1px solid #000;
			border-top: 1px solid #000;
			border-bottom: 1px solid #000;
		}
		.normal_table1 th {
			border-left: 1px solid #000;
			border-right: 1px solid #000;
		}

        
        .normal_table_header1 tr th {
        	font-size:28pt;
        	font-family: "arial";
        	text-align:center;
        }
        .normal_table_header1 tr td {
        	font-size:25pt;
        	font-family: "arial";
        	text-align:left;
        }
        .normal_table tr td {
        	font-size:22pt;
        	font-family: "arial";
        	border:3px solid black;
        	text-align:center;
        }
        .normal_table tr th {
        	font-size:22pt;
        	font-family: "arial";
        	border:3px solid black;
        	text-align:center;
        }
        .sec_table tr td {
        	font-size:22pt;
        	font-family: "arial";
        	border:3px solid black;
        	text-align:left;
        }
        .sec_table tr th {
        	font-size:22pt;
        	font-family: "arial";
        	text-align:left;
        }
        .sec_table1 tr th {
        	font-size:22pt;
        	font-family: "arial";
        	text-align:left;
        }
        .sec_table1 tr td {
        	font-size:22pt;
        	font-family: "arial";
        	text-align:left;
        }        
    </style>
</head>
<body>
    %for o in objects :
		<table class="normal_table_header1" width="100%" height="100%">
			<tr>
				<th colspan="36">MINISTRY / DEPARTMENT -FEDERAL  JUDICIAL SERVICE COMMISION</th>
			</tr>
			<tr>
				<th colspan="36">NIGERIA FEDERAL  GOVERNMENT</th>
			</tr>
			<tr>
				<th colspan="36">PAYROLL</th>
			</tr>
			<tr>
				<td></td>
			</tr>
			<tr>
				<td></td>
			</tr>			
			<tr>
				<td></td>
			</tr>
			<tr>
				<td colspan="36"><b>T.F.2 PRB (1973)</b></td>
			</tr>
			<tr>
				<td colspan="36"><b>Date From : ${call_date_from(o)} To  ${call_date_to(o)}</b></td>
			</tr>
			<tr>
				<td colspan="36"><b>${ get_name(o)}</b></td>
			</tr>
			<tr>
				<td></td>
			</tr>
			<tr>
				<td colspan="36"><b>Sheet Number</b></td>
			</tr>
			<tr>
				<td><font style="color:white">......</font></td>
			</tr>			
        	<tr>
        		<td colspan="36">
        			<table class="normal_table1" width="100%" height="100%">
				    	<tr>
							<td colspan="4">  <b>EARNINGS</b> </td>
							<td colspan="14">  <b>DEDUCTION 'A' AND 'B'</b> </td>
							<td colspan="18">  <b>ALLOWANCE</b> </td>
						</tr>
						<tr>
							<th>Consolidated Salary</th>
				            <th>ACTINGALW.</th>
				            <th>OVERTIME</th>
				            <th>GROSS EMOLUMENTS</th>
				            <th>TAX THIS MONTH</th>
				            <th>NHF</th>
				            <th>OTHER DED.</th>
				            <th>PENSION</th>
				            <th>NHIS</th>
				            <th>C.T.L.S</th>
				            <th>MV ADV INT.</th>
				            <th>UGV PERS. ADV.</th>
				            <th>FGHB</th>
				            <th>OVER PAYMENT</th>
				            <th>SALARY ADVANCE</th>
				            <th>TOTAL DEDUCATION</th>
				            <th>NET PAY</th>
				            <th>MEAL SUBSIDY</th>
				            <th>RENT SUBSIDY</th>
				            <th>TRANS. ALW</th>
				            <th>FURN. ALW</th>
				            <th>DOM. SERV. ALW</th>
				            <th>ENT. ALW</th>
				            <th>ACCOM. ALW</th>
				            <th>PERS ASSIS. ALW</th>
				            <th>MOTOR ALW</th>
				            <th>NEWS. ALW</th>
				            <th>UTILITY</th>
				            <th>ANNUAL LEAVE GRANT</th>
				            <th>Peculiar Allowance</th>
				            <th>UNDER PAYMENT</th>
				            <th>ARREARS Allowance</th>
				            <th>TOTAL NON TAXABLE</th>
				            <th>TOTAL NET EMOLUMENTS</th>
				            <th>NAME</th>
				            <th>SIGN</th>
						</tr>
						%for line in (get_payslip_lines(o)):
				        <tr>
				        	<td>
				                 N ${line.get('basic') or '0.00'}
				             </td>
				            <td>
				                N ${line.get('acting_allow') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('overtime') or '0.00'}
				            </td>
				            <td>
				               N ${line.get('gross_amount') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('tax') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('nhf') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('other_ded') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('pension') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('nhis') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('ctls') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('mv_adv_interest') or '0.00'}
				            <td>
				                N ${line.get('personl_adv') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('fghb') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('over_payment') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('salary_advance') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('deducation_amt') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('net_pay') or '0.00'}
				            </td>
				            <td>
				                N ${'0.00'}
				            </td>
				            <td>
				                N ${'0.00'}
				            </td>
				            <td>
				                N ${'0.00'}
				            </td>
				            <td>
				                N ${'0.00'}
				            </td>
				            <td>
				                N ${'0.00'}
				            </td>
				            <td>
				                N ${'0.00'}
				            </td>
				            <td>
				                N ${'0.00'}
				            </td>
				            <td>
				                N ${'0.00'}
				            </td>
				            <td>
				               N ${'0.00'}
				            </td>
				            <td>
				                N ${'0.00'}
				            </td>
				            <td>
				               N ${'0.00'}
				            </td>
				            <td>
				                N ${'0.00'}
				            </td>
				            <td>
				                N ${line.get('peculiar') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('underpayment') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('arrear_basic') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('taxable') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('net_total') or '0.00'}
				            </td>
				            <td>
				                ${line.get('name') or ' '}
				            </td>
				            <td>
				            </td>
				        </tr>
				        %endfor
				        %for line in (get_total(o)):
						    <tr>
						    	<td><b>N ${line.get('basic') or '0.00'}</b></td>
						    	<td><b>N ${line.get('acting_allow') or '0.00'}</b></td>
						    	<td><b>N ${line.get('overtime') or '0.00'}</b></td>
						    	<td><b>N ${line.get('gross_amount') or '0.00'}</b></td>
						    	<td><b>N ${line.get('tax') or '0.00'}</b></td>
						    	<td><b>N ${line.get('nhf') or '0.00'}</b></td>
						    	<td><b>N ${line.get('other_ded') or '0.00'}</b></td>
						    	<td><b>N ${line.get('pension') or '0.00'}</b></td>
						    	<td><b>N ${line.get('nhis') or '0.00'}</b></td>
						    	<td><b>N ${line.get('ctls') or '0.00'}</b></td>
						    	<td><b>N ${line.get('mv_adv_interest') or '0.00'}</b></td>
						    	<td><b>N ${line.get('personl_adv') or '0.00'}</b></td>
						    	<td><b>N ${line.get('fghb') or '0.00'}</b></td>
						    	<td><b>N ${line.get('over_payment') or '0.00'}</b></td>
						    	<td><b>N ${line.get('salary_advance') or '0.00'}</b></td>
						    	<td><b>N ${line.get('deducation_amt') or '0.00'}</b></td>
						    	<td><b>N ${line.get('net_pay') or '0.00'}</b></td>
						    	<td><b>N ${'0.00'}</b></td>
						    	<td><b>N ${'0.00'}</b></td>
						    	<td><b>N ${'0.00'}</b></td>
						    	<td><b>N ${'0.00'}</b></td>
						    	<td><b>N ${'0.00'}</b></td>
						    	<td><b>N ${'0.00'}</b></td>
						    	<td><b>N ${'0.00'}</b></td>
						    	<td><b>N ${'0.00'}</b></td>
						    	<td><b>N ${'0.00'}</b></td>
						    	<td><b>N ${'0.00'}</b></td>
						    	<td><b>N ${'0.00'}</b></td>
						    	<td><b>N ${'0.00'}</b></td>
						    	<td><b>N ${line.get('peculiar') or '0.00'}</b></td>
						    	<td><b>N ${line.get('underpayment') or '0.00'}</b></td>
						    	<td><b>N ${line.get('arrear_basic') or '0.00'}</b></td>
						    	<td><b>N ${line.get('taxable') or '0.00'}</b></td>
						    	<td><b>N ${line.get('net_total') or '0.00'}</b></td>
						    	<td><b>Total</b></td>
						    	<td></td>
						    </tr>
				        %endfor
        			</table>
        		</td>
        	</tr>
        </table>
    %endfor
</body>
</html>
