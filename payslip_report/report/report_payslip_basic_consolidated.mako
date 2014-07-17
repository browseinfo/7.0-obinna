<html>
<head>
    <style type="text/css">
       ${css}
   </style>
</head>
<body>
%for o in objects :
	<center><h1>FEDERAL JUDICIAL SERVICE COMMISSION STAFF PAYSLIP</h1></center>
		<table align="right">
			<tr>
				<td><b>Date From :   </b>  ${call_date_from(o)}</td>
				<td><b>-   </b>  ${call_date_to(o)}</td>
			</tr>
		</table>
		<br>
		<br>
        <table align="center" width="50%">
            <tbody>
            	<tr>
                <tr>
                    <th style="text-align:right;">${_("Year")}</th>
                    <th style="text-align:center;"> - </th>
                    <th style="text-align:left;">${get_year(o)} </th>
                </tr>
                <tr>
                    <th style="text-align:right;">${_("Month")}</th>
                    <th style="text-align:center;"> - </th>
                    <th style="text-align:left;">${get_year_month(o)} </th>
                </tr>
                <tr>
                    <th style="text-align:right;">${_("File Num")}</th>
                    <th style="text-align:center;"> - </th>
                    <th style="text-align:left;">${get_file_number(o)}</th>
                </tr>
                <tr>
                    <th style="text-align:right;" >${_("Name")}</th>
                    <th style="text-align:center;"> - </th>
                    <th style="text-align:left;">${get_name(o)}</th>
                </tr>
                <tr>
                    <th style="text-align:right;" >${_("Sex")}</th>
                    <th style="text-align:center;"> - </th>
                    <th style="text-align:left;">${get_sex(o)}</th>
                </tr>
                <tr>
                    <th style="text-align:right;" >${_("Step")}</th>
                    <th style="text-align:center;"> - </th>
                    <th style="text-align:left;">${get_step(o)}</th>
                </tr>
                <tr>
                    <th style="text-align:right;" >${_("Grade")}</th>
                    <th style="text-align:center;"> - </th>
                    <th style="text-align:left;">${get_grade(o)}</th>
                </tr>
                <tr>
                    <th style="text-align:right;" >${_("Bank")}</th>
                    <th style="text-align:center;"> - </th>
                    <th style="text-align:left;">${get_bank(o)}</th>
                </tr>
                <tr>
                    <th style="text-align:right;" >${_("Account No.")}</th>
                    <th style="text-align:center;"> - </th>
                    <th style="text-align:left;">${get_acc_no(o)}</th>
                </tr>
                <tr>
                    <th style="text-align:right;" >${_("Sort Code")}</th>
                    <th style="text-align:center;"> - </th>
                    <th style="text-align:left;">${get_sort_code(o)}</th>
                </tr>
                </tr>
            </tbody>
        </table>
        <table>
	<table border="1" style="width:600px">
		<tr>
			<td>
				<table border="1" style="width:600px">
					<tr>
				  		<td colspan="2"><b>Consolidated Salary</b></td>
				  	</tr>
					<tr>
				  		<td>Consolidated Salary</td>
				  		<td>${get_payslip_lines(o.line_ids)['consolidated_salary']} </td>		
					</tr>
					<tr>
						<td>Over Time </td>
						<td>${get_payslip_lines(o.line_ids)['overtime'] or '0.0'} </td>
					</tr>
					<tr>
						<td>Arrears Basic</td>
						<td>${get_payslip_lines(o.line_ids)['arrear']}  </td>
					</tr>
					<tr>
						<td><b>Total Consolidated Salary</b> </td>
						<td>${get_payslip_lines(o.line_ids)['total_consolidated_salary']} </td>
					</tr>
					<tr>
						<td><b>Allowance</b> </td>
						<td> </td>
					</tr>
					<tr>
						<td>Peculiar Allowance </td>
						<td>${get_payslip_lines(o.line_ids)['peculiar'] or '0.0'}</td>
					</tr>
					<tr>
						<td>Arrear Allowance </td>
						<td>${get_payslip_lines(o.line_ids)['arrear_allowance'] or '0.0'}</td>
					</tr>	
					<tr>
						<td>Under Payment </td>
						<td>${get_payslip_lines(o.line_ids)['underpayment'] or '0.0'}</td>
					</tr>
									
				    <tr>
					    <td><b>Total Allowance</b> </td>
					    <td>${get_payslip_lines(o.line_ids)['total_allowance'] or '0.0'}</td>
				    </tr>
				</table>
				<table>
			    	<tr class="noBorder">
					<td>
						<table>
								<tr><td><font color="white">.</font></td></tr>
								<tr><td><font color="white">.</font></td></tr>
								<tr><td><font color="white">.</font></td></tr>		
								<tr><td><font color="white">.</font></td></tr>
								<tr><td><font color="white">.</font></td></tr>
						</table>
					</td>
				</tr>
			    </table>
		</td>
		<td>
		<table border="1" style="width:690px">
				  <tr>
				  	<td colspan="2"><b>Deduction</b></td>
				  </tr>
				<tr>
				  <td>Tax</td>
				  <td>${get_payslip_lines(o.line_ids)['tax'] or '0.0'} </td>		
				</tr>
				<tr>
					<td>Rent </td>
					<td>${get_payslip_lines(o.line_ids)['rent'] or '0.0'} </td>
				</tr>
				<tr>
					<td>Over Payment </td>
					<td>${get_payslip_lines(o.line_ids)['over'] or '0.0'} </td>
				</tr>
				<tr>
					<td>Pension</td>
					<td>${get_payslip_lines(o.line_ids)['pension'] or '0.0'} </td>
				</tr>
				<tr>
					<td>NHF</td>
					<td>${get_payslip_lines(o.line_ids)['nhf'] or '0.0'} </td>
				</tr>
				<tr>
					<td>CTLS </td>
					<td>${get_payslip_lines(o.line_ids)['ctls'] or '0.0'} </td>
				</tr>
				<tr>
					<td>NHIS </td>
					<td>${get_payslip_lines(o.line_ids)['nhis'] or '0.0'} </td>
				</tr>
				
				<tr>
					<td>Salary Advance</td>
					<td>${get_payslip_lines(o.line_ids)['salary'] or '0.0'} </td>
				</tr>
				<tr>
					<td>Motor Vehicle Advance </td>
					<td>${get_payslip_lines(o.line_ids)['motor'] or '0.0'} </td>
				</tr>
				<tr>
					<td>FGHB </td>
					<td>${get_payslip_lines(o.line_ids)['fghb'] or '0.0'} </td>
				</tr>
				<tr>
					<td>Other Deductions </td>
					<td>${get_payslip_lines(o.line_ids)['other'] or '0.0'} </td>
				</tr>
				<tr>
					<td>Personal Advance</td>
					<td>${get_payslip_lines(o.line_ids)['personal'] or '0.0'} </td>
				</tr>
				<tr>
					<td><b>Total Deductions</b> </td>
					<td>${get_payslip_lines(o.line_ids)['deductions'] or '0.0'} </td>
				</tr>

				</table>
				
				
		</td>
		</tr>
	        <tr>
	            <td> 	
			        <table border="1" style="width:600px">			    
					    <tr>
					        <td><b>Gross Emolument</b> </td>
					        <td>${get_payslip_lines(o.line_ids)['consolidated']} </td>
				        </tr>
				    </table>		 
				</td>
			    <td>
				    <table border="1" style="width:600px">	
				    <tr>
					    <td><b>Net Emoluments</b> </td>
					    <td>${get_payslip_lines(o.line_ids)['net_emoluments'] or '0.0'} </td>
				    </tr>
				    </table>
			    </td>
		    </tr>
		</table>
		%endfor 
		</table>
</body>
</html>
