<html>
<head>
    <style type="text/css">
        ${css}
        
        .normal_table1 {
			border:none;
			border-collapse: collapse;
		}

		.normal_table1 td {
			border-left: 9px solid #000;
			border-right: 9px solid #000;
			border-top: 9px solid #000;
			border-bottom: 9px solid #000;
		}
		.normal_table1 th {
			border-left: 9px solid #000;
			border-right: 9px solid #000;
		}

        .normal_table_header1 tr th {
        	font-size:140pt;
        	font-family: "arial";
        	text-align:center;
        }
        .normal_table_header1 tr td {
        	font-size:120pt;
        	font-family: "arial";
        	text-align:left;
        }
        .normal_table tr td {
        	font-size:100pt;
        	font-family: "arial";
        	border:9px solid #000;
        	text-align:center;
        }
        .normal_table tr th {
        	font-size:100pt;
        	font-family: "arial";
        	border:9px solid #000;
        	text-align:center;
        }
        .sec_table tr td {
        	font-size:100pt;
        	font-family: "arial";
        	border:9px solid #000;
        	text-align:left;
        }
        .sec_table tr th {
        	font-size:100pt;
        	font-family: "arial";
        	text-align:left;
        }
        .sec_table1 tr th {
        	font-size:100pt;
        	font-family: "arial";
        	text-align:left;
        }
        .sec_table1 tr td {
        	font-size:100pt;
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
				<th colspan="36">BASIC PAYROLL SUMMARY</th>
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
				<td colspan="36"><b>Nigeria Federal Government</b></td>
			</tr>
			<tr>
				<td colspan="36"><b>FGP 645/979/100.000 (OL 2890)</b></td>
			</tr>
			<tr>
				<td colspan="36"><b>${get_bank()}</b></td>
			</tr>
			<tr>
				<td></td>
			</tr>
			<tr>
				<td colspan="36"><b>SHEET NO ...........................</b></td>
			</tr>
			<tr>
				<td colspan="36"><b>MONTH ENDING</b> :${get_month(o)} <b>YEAR</b> ${o.period_id.date_start.split('-')[0]}</td>
			</tr>
			<tr>
				<td><font style="color:white">......</font></td>
			</tr>			
        	<tr>
        		<td colspan="36">
        			<table class="normal_table1" width="100%" height="100%">
				    	<tr>
							<td colspan="4">  <b>EARNINGS</b> </td>
							<td colspan="14">  <b>DEDUCTION</b> </td>
							<td colspan="18">  <b>ALLOWANCE</b> </td>
						</tr>
						<tr>
							<th>BASIC SALARY</th>
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
				            <th>NIGERIAN REGION</th>
				            <th>FGHB</th>
				            <th>OVER PAYMENT</th>
				            <th>SALARY ADVANCE</th>
				            <th>TOTAL DEDUCATION</th>
				            <th>NET PAY</th>
				            <th>MEAL SUBSIDY</th>
				            <th>RENT SUBSIDY</th>
				            <th>TRANS. ALW</th>
				            <th>FURN. ALW</th>
				            <th>ENT. ALW</th>
				            <th>ACCOM. ALW</th>
				            <th>UNDER PAYMENT ALW</th>
				            <th>PERS ASSIS. ALW</th>
				            <th>MOTOR ALW</th>
				            <th>NEWS. ALW</th>
				            <th>UTILITY</th>
				            <th>DOM. SERV. ALW</th>
				            <th>ANNUAL LEAVE GRANT</th>
				            <th>ARREARS ALW</th>
				            <th>PERCULIAR ALW</th>
				            <th>UNDER PAYMENT</th>
				            <th>TOTAL NON TAXABLE</th>
				            <th>TOTAL NET EMOLUMENTS</th>
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
				                ${line.get('nhis') or '0.00'}
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
				                N ${line.get('nigerin_reg') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('fghb') or '0.00'}
				            </td>
				            <td>
				                ${line.get('over_payment') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('salary_advance') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('deducation_amt') or '0.00'}
				            </td>
				            <td>
				                ${line.get('net_pay') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('meal') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('rent') or '0.00'}
				            </td>
				            <td>
				                ${line.get('transport') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('furniture') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('entertainment') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('accomodation') or '0.00'}
				            </td>
				            <td>
				                ${line.get('under_payment') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('personal_alw') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('motor_allw') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('newspaper') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('utilities') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('domestic_servent') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('leave_grant') or '0.00'}
				            </td>
				            <td>
				                ${line.get('arrears') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('peculiar') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('under_payment') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('taxable') or '0.00'}
				            </td>
				            <td>
				                N ${line.get('net_total') or '0.00'}
				            </td>
				        </tr>
				        %endfor
        			</table>
        		</td>
        	</tr>
        	<tr>
        		<td><font style="color:white">......</font></td>
        	</tr>
        	<tr>
        		<td>
        			<b>MINISTRY / DEPARTMENT P.V. No.................. MONTH OF 
        			${get_month(o)}&nbsp;&nbsp;${o.period_id.date_start.split('-')[0]}</b>
        		</td>
        	</tr>
        	<tr>
        		<td><font style="color:white">......</font></td>
        	</tr>
			<tr>
				<td colspan="6">
					<table class="sec_table" width="80%">
						<tr>
							<td><b>DETAIL</b></td>
							<td><b>SIGNATUR</b></td>
							<td><b>NAME <br/>IN BLOCK <br/>LETTER</b></td>
							<td><b>DATE</b></td>
						</tr>
						<tr><td>Prrepared<br/>by</td><td></td><td></td><td></td></tr>
						<tr><td>Checked<br/>by</td><td></td><td></td><td></td></tr>
						<tr><td>Entered in</br/>Vote Book</td><td></td><td></td><td></td></tr>
						<tr><td>Passed<br/>by</td><td></td><td></td><td></td></tr>
						<tr><td>Paid<br/>by</td><td></td><td></td><td></td></tr>					
					</table>				
				</td>
				<td colspan="6">
					<table class="sec_table" width="80%">
						<tr>
							<th colspan="2">PAYMENT VOUCHER EMOLUMENTS</th>
						</tr>
						%for line in (get_payslip_lines(o)):
						<tr>
							<td>
								GROSS EMOLUMENTS for the month to..........
							</td>
							<td>N ${line.get('gross_amount') or '0.00'}</td>
						</tr>
						<tr>
							<td>
								MOTOR BASIC ALLOWANCE for the month to..........
							</td>
							<td>N ${line.get('taxable') or '0.00'}</td>
						</tr>
						<tr>
							<td>
								GROSS PAYMENT PER VOUCHER
							</td>
							<td>N ${ line.get('gross_amount')+line.get('taxable') }</td>
						</tr>
						<tr>
							<td>
								Recoveries from officer
							</td>
							<td></td>
						</tr>
						<tr>
							<td>INCOMETAX</td>
							<td>N ${line.get('tax') or '0.00'}</td>
						</tr>
						<tr>
							<td>INCOME RATE</td>
							<td>N ${'0.00'}</td>
						</tr>
						<tr>
							<td>CTLS</td>
							<td>N ${line.get('ctls') or '0.00'}</td>
						</tr>
						<tr>
							<td>MORTGAGE SAVINGS</td>
							<td>N ${'0.00'}</td>
						</tr>
						<tr>
							<td>Rent & Wear</td>
							<td>N ${'0.00'}</td>
						</tr>
						<tr>
							<td>M.V. Advance Including Interest</td>
							<td>N ${line.get('mv_adv_interest') or '0.00'}</td>
						</tr>
						<tr>
							<td>FGHB Advance Including Interest</td>
							<td>N ${line.get('fghb') or '0.00'}</td>
						</tr>
						<tr>
							<td>Personal Advance</td>
							<td>N ${line.get('personl_adv') or '0.00'}</td>
						</tr>
						<tr>
							<td>Other Deduction</td>
							<td>N ${line.get('other_ded') or '0.00'}</td>
						</tr>
						<tr>
							<td>MV Refurb. Loan </td>
							<td>N ${'0.00'}</td>
						</tr>
						<tr>
							<td>Staff Transport Deduction</td>
							<td>N ${'0.00'}</td>
						</tr>
						<tr>
							<td>NHIS</td>
							<td>N ${line.get('nhis') or '0.00'}</td>
						</tr>
						<tr>
							<td>PENSION</td>
							<td>N ${line.get('pension') or '0.00'}</td>
						</tr>
						<tr>
							<td>Salary Advance Recovery</td>
							<td>N ${line.get('salary_advance') or '0.00'}</td>
						</tr>
						<tr>
							<td>NHF</td>
							<td>N ${line.get('nhf') or '0.00'}</td>
						</tr>
						<tr>
							<td>Over Payment</td>
							<td>N ${line.get('over_payment') or '0.00'}</td>
						</tr>
						<tr>
							<td>Nigerion Region</td>
							<td>N ${line.get('nigerin_reg') or '0.00'}</td>
						</tr>
						<tr>
							<td>MISCELLANEOUS: C</td>
							<td>N ${'0.00'}</td>
						</tr>
						<tr>
							<td>MISCELLANEOUS: D</td>
							<td>N ${'0.00'}</td>
						</tr>
						<tr>
							<td>TOTAL RECOVERS ON VOUCHER</td>
							<td>N ${ line.get('deduct_voucher') or '0.00' } </td>
						</tr>
						%endfor
					 </table>				
				</td>
				<td colspan="6">
					<table class="sec_table">
						<tr><th>HEAD_________SUBHEAD________</th></tr>
						<tr><th>HEAD_________SUBHEAD________</th></tr>
						<tr><td><b>REVENUE ACCOUNT CREDITED</b></td></tr>
						<tr>
							<td><b>HEAD_________SUBHEAD________</b></td>
						</tr>
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>	
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>	
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>	
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>	
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>	
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>	
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>	
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>			
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>	
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>	
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>	
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>	
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>	
						<tr>
							<td>HEAD_________SUBHD________</td>
						</tr>															
					</table>				
				</td>
				<td colspan="9">
					<table class="sec_table" width="80%">
						<tr>
							<td><b>SALARY DEDUCTION ADV. NO</b></td>
							<td><b>ON PAYT DEPT/MIN P.V. NO</b></td>
						</tr>
						<tr>
							<td><font style="color:white">......</font></td>
							<td><font style="color:white">......</font></td>
						</tr>
						<tr>
							<td><font style="color:white">......</font></td>
							<td><font style="color:white">......</font></td>
						</tr>
						<tr>
							<td><font style="color:white">......</font></td>
							<td><font style="color:white">......</font></td>
						</tr>
						<tr>
							<td><font style="color:white">......</font></td>
							<td><font style="color:white">......</font></td>
						</tr>
						<tr>
							<td><font style="color:white">......</font></td>
							<td><font style="color:white">......</font></td>
						</tr>
						<tr>
							<td><font style="color:white">......</font></td>
							<td><font style="color:white">......</font></td>
						</tr>
						<tr>
							<td><font style="color:white">......</font></td>
							<td><font style="color:white">......</font></td>
						</tr>
					</table>					
				</td>
				<td colspan="9">
					<table class="sec_table" width="80%">
						<tr>
							<td><b>P.V. NO</b></td>
							<td><b>MONTH/YEAR</b></td>
							<td><b>PAYABLE AT</b></td>						
						</tr>
						<tr>
							<td><font style="color:white">......</font><br/><br/><br/><br/><br/></td>
							<td><font style="color:white">......</font><br/><br/><br/><br/><br/></td>
							<td><font style="color:white">......</font><br/><br/><br/><br/><br/></td>						
						</tr>					
					</table>				
				</td>
        	</tr>
        	<tr>
				<td colspan="6">
					<table class="sec_table" width="80%">
						<tr>
							<td colspan="2">
								<b>
									&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
									INTERNAL AUDIT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
								</b>
							</td>
						</tr>
						<tr>
							<td>
								&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;STAMP&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
								<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
							</td>
							<td>
								&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;DATE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
								<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
							</td>
						</tr>
					</table>				
				</td>
				<td colspan="6"></td>
				<td colspan="6"></td>
				<td colspan="9"></td>
				<td colspan="9">
					<table class="sec_table1" width="80%">
						<tr><th>PAYMENT AUTHORISATION<br/></th></tr>
						<tr>
							<td>I HEREBY CERTIFY THAT the above is a<br/>
								correct statement of the amount pay-able to the person named on<br/>
								Min./Dept.<br/>
								Payroll Sheet Nos..........................................<br/>
								for the month ending
								...............................................................20.......
								That their employment at the rate of<br/>
								salary shown was duly authorised</br>
								by......................................................................<br/>
								the amount of .........................................<br/>
								..................................................................Naira<br/>
								..........................Kobo may be be paid under
								the Heads and items shown.<br/>
								.........................................................Signature<br/>
								.................................................................Title<br/>
								............................................................20........<br/>
								TO BE SIGNED BY DULY AUTHORISED OFFICER
							</td>
						</tr>					
					</table>	
				</td>
			</tr>
			<tr>
				<td colspan="6">
					<table class="sec_table" width="80%">
						<tr>
							<th>
								AMOUNT OF CHEQUE PAYABLE ...........N ${total()}<br/>AMOUNT IN WORDS  ....${amount_word()}
							</th>
						</tr>
					</table>
				</td>
			</tr>
        </table>
        
    %endfor
</body>
</html>
