package main
import (
    "fmt"
    "github.com/denverdino/aliyungo/dns"
    "os"
    "time"
)
var certbot_ali_key string
var certbot_ali_secret string
func init() {
    // 定义阿里云的访问key和secret
    certbot_ali_key = os.Getenv("CERTBOT_ALI_KEY")
    certbot_ali_secret = os.Getenv("CERTBOT_ALI_SECRET")
    // 判断阿里云的key和secret是否存在
    if certbot_ali_key == "" || certbot_ali_secret == "" {
        fmt.Println("请设置环境变量CERTBOT_ALI_KEY和CERTBOT_ALI_SECRET")
        os.Exit(1)
    }
}
func main() {
    client := dns.NewClient(certbot_ali_key, certbot_ali_secret)
    var args = new(dns.DescribeDomainRecordsArgs)
    args.DomainName = os.Getenv("CERTBOT_DOMAIN")
    args.RRKeyWord = "_acme-challenge"
    args.TypeKeyWord = "TXT"
    res, err := client.DescribeDomainRecords(args)
    if err == nil {
        records := res.DomainRecords.Record
        // 记录大于1执行更新，小于1执行创建
        if len(records) > 0 {
            for i := 0; i < len(records); i++ {
                var update_args = new(dns.UpdateDomainRecordArgs)
                update_args.RecordId = records[i].RecordId
                update_args.RR = "_acme-challenge"
                update_args.Value = os.Getenv("CERTBOT_VALIDATION")
                update_args.Type = "TXT"
                res, err := client.UpdateDomainRecord(update_args)
                if err == nil {
                    fmt.Println("更新成功:", res.RecordId)
                    time.Sleep(time.Duration(20) * time.Second)
                } else {
                    fmt.Println("更新失败:", err.Error())
                    os.Exit(2)
                }
            }
        } else {
            // 执行创建操作
            var add_args = new(dns.AddDomainRecordArgs)
            add_args.DomainName = os.Getenv("CERTBOT_VALIDATION")
            add_args.RR="_acme-challenge"
            add_args.Value=os.Getenv("CERTBOT_VALIDATION")
            add_args.Type="TXT"
            res,err:=client.AddDomainRecord(add_args)
            if err == nil {
                fmt.Println("创建成功:", res.RecordId)
                time.Sleep(time.Duration(20) * time.Second)
            } else {
                fmt.Println("创建失败:", err.Error())
                os.Exit(2)
            }
        }
    }
}
