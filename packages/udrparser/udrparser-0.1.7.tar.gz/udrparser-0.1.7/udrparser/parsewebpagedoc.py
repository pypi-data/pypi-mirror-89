import pandas as pd
import lxml.html as html
import re
import socket


class udrparser:
    def getdoctables():
        # pd.set_option("display.max_rows", 1000)
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.width', None)
        # pd.set_option('display.max_colwidth', None)

        url = "https://www.docs.microsoft.com/en-us/azure/databricks/administration-guide/cloud-configurations/azure/udr"
        pdhtml = pd.read_html(url, header=0)[2]
        tmp = pdhtml.to_html()
        content = html.fromstring(tmp)

        tr_elements = content.xpath("//tbody/tr")
        column_headers = []

        header = ["Azure Databricks Workspace Region", "Service", "FQDN"]
        for column in header:  # tr_elements[0]:
            #     name = column.text_content()
            column_headers.append((column, []))

        for row in range(0, len(tr_elements)):
            table_tr = tr_elements[row]
            column_count = 0

            for column in table_tr.iterchildren():
                string = column.text_content()

                if string.count("net") > 1:
                    data = re.sub(r"net", r"net\n", string)
                    data = data.split("\n")
                    for word in data:
                        column_headers[column_count][1].append(word)
                elif string.count("com") > 1:
                    data = re.sub(r"com", r"com\n", string)
                    data = data.split("\n")
                    for word in data:
                        column_headers[column_count][1].append(word)
                else:
                    data = column.text_content()
                    column_headers[column_count][1].append(data)

            column_count += 1

        dictionary = {title: column for (title, column) in column_headers}
        df = pd.DataFrame.from_dict(dictionary, orient="index")  # from_dict
        df = df.transpose()
        df = df.drop(df.columns[[1, 2]], axis=1)
        df.dropna
        df = df[
            pd.to_numeric(
                df["Azure Databricks Workspace Region"], errors="coerce"
            ).isnull()
        ]
        finaldf = df[df["Azure Databricks Workspace Region"] != "NaN"]
        return finaldf

    def tryconvert(fqdn):
        try:
            if fqdn is None:
                return None
            else:
                ipaddr = socket.gethostbyname_ex(fqdn)[2]
                lst = [ip + "/32" for ip in ipaddr]
                return lst
        except:
            pass
