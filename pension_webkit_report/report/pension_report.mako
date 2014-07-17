<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    %for o in objects :
		<table  width="600%">
		<tr>
			<td ><table>
				<tr><td> <font style="font-size:90px; text-align:center;"><b>NIGERIA FEDERAL  GOVEREMENT PAYROLL</b></font></td></tr>
				<tr><td> <font style="font-size:80px; text-align:center;"> PENSION REPORT</font></td></tr>
				<tr><td> <font style="font-size:70px; text-align:center;"> Date From : ${call_date_from(o)} -  ${call_date_to(o)}</font></td></tr>
			</table> </td>
		</tr>
		
	</table>
<br/><br/><br/>
        <table class="list_table" width="600%">
            <thead>
                <tr>
                    <th style="font-size:70px; text-align:center;"> ${_("S/N")}</th>
                    <th style="font-size:70px; text-align:left;">${_("Staff Name")}</th>
                    <th style="font-size:70px; text-align:left;"> ${_("Rank")}</th>
                    <th style="font-size:70px; text-align:left;"> ${_("GL")}</th>
                    <th style="font-size:70px; text-align:right;">${_("Amount")}</th>
                </tr>
            </thead>
            %for line in (get_payslip_lines(o)):
                <tbody >
                <tr>
                    <td style="font-size:50px; text-align:center;border-collapse:collapse; ">
                         ${get_seq()}
                     </td>
                    <td style="font-size:50px; text-align:left;border-collapse:collapse;">	
                        ${line.get('name') or ''}
                    </td>
                    <td style="font-size:50px; text-align:left;border-collapse:collapse;"">
                        ${line.get('step_name') or ''}
                    </td>
                    <td style="font-size:50px; text-align:left;border-collapse:collapse;">
                        ${line.get('grade_name') or ''}
                    </td>
                    <td style="font-size:50px; text-align:right;border-collapse:collapse;">
                        ${line.get('pension') or ''}
                    </td>
                </tr>
                </tbody>
            %endfor
		%for line in (get_total(o)):
		<tbody >
                <tr>
                    <td style="text-align:left;border-collapse:collapse; "><font size="8"> <b>
                          </b></font>
                     </td>
                    <td style="text-align:left;border-collapse:collapse;"><font size="8"> <b>
                       </b></font>
                    </td>
                    <td style="text-align:left;border-collapse:collapse;""><font size="8"> <b>
                        </b></font>
                    </td>
                    <td style="text-align:left;border-collapse:collapse;"><font size="8"> <b>
                       </b></font>
                    </td>
                    <td style="font-size:70px; text-align:right;border-collapse:collapse;"><b>
                        ${line.get('pension') or ''}</b>
                    </td>
                </tr>
		</tbody >
		%endfor	
        </table>
 
    %endfor
</body>
</html>
