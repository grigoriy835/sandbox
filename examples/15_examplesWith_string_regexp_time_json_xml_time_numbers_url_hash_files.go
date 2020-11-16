package main

import (
	"bufio"
	"bytes"
	"crypto/sha1"
	b64 "encoding/base64"
	"encoding/json"
	"encoding/xml"
	"fmt"
	"io"
	"io/ioutil"
	"math/rand"
	"net"
	"net/url"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	s "strings"
	"time"
)

var p = fmt.Println

func main() {
	print("start\n")

	stringFunctions()
	stringFormating()
	regularExp()
	jsonUsage()
	xmlUsage()

	datetimeFormatting()
	unixtimeFormatting()
	timeParsing_formatting()

	randomNumberGeneration()
	numberParsing()

	urlParsing()
	sha1Generation()
	base64EncDec()

	fileParsing()
	fileWriting()
	filePathes()
	tempFileDir()

	lineFilters()

}

func stringFunctions() {
	p("Contains:  ", s.Contains("test", "es"))
	p("Count:     ", s.Count("test", "t"))
	p("HasPrefix: ", s.HasPrefix("test", "te"))
	p("HasSuffix: ", s.HasSuffix("test", "st"))
	p("Index:     ", s.Index("test", "e"))
	p("Join:      ", s.Join([]string{"a", "b"}, "-"))
	p("Repeat:    ", s.Repeat("a", 5))
	p("Replace:   ", s.Replace("foo", "o", "0", -1))
	p("Replace:   ", s.Replace("foo", "o", "0", 1))
	p("Split:     ", s.Split("a-b-c-d-e", "-"))
	p("ToLower:   ", s.ToLower("TEST"))
	p("ToUpper:   ", s.ToUpper("test"))
	p()

	p("Len: ", len("hello"))
	p("Char:", "hello"[1])
}

func stringFormating() {

	type point struct {
		x, y int
	}

	po := point{1, 2}

	fmt.Printf("%v\n", po)                     //{1 2}
	fmt.Printf("%+v\n", po)                    //{x:1 y:2}
	fmt.Printf("%#v\n", po)                    //main.point{x:1, y:2}
	fmt.Printf("%T\n", po)                     //main.point
	fmt.Printf("%t\n", true)                   //true
	fmt.Printf("%d\n", 123)                    //123
	fmt.Printf("%b\n", 14)                     //1110
	fmt.Printf("%c\n", 33)                     //!
	fmt.Printf("%x\n", 456)                    //	1c8
	fmt.Printf("%f\n", 78.9)                   //78.900000
	fmt.Printf("%e\n", 123400000.0)            //1.234000e+08
	fmt.Printf("%E\n", 123400000.0)            //1.234000E+08
	fmt.Printf("%s\n", "\"string\"")           //"string"
	fmt.Printf("%q\n", "\"string\"")           //"\"string\""
	fmt.Printf("%x\n", "hex this")             //6865782074686973
	fmt.Printf("%p\n", &p)                     //0x42135100
	fmt.Printf("|%6d|%6d|\n", 12, 345)         //|    12|   345|
	fmt.Printf("|%6.2f|%6.2f|\n", 1.2, 3.45)   //|  1.20|  3.45|
	fmt.Printf("|%-6.2f|%-6.2f|\n", 1.2, 3.45) //|1.20  |3.45  |
	fmt.Printf("|%6s|%6s|\n", "foo", "b")      //|   foo|     b|
	fmt.Printf("|%-6s|%-6s|\n", "foo", "b")    //|foo   |b     |
	ss := fmt.Sprintf("a %s", "string")
	fmt.Println(ss) //a string

	fmt.Fprintf(os.Stderr, "an %s\n", "error") //an error
}

func regularExp() {
	match, _ := regexp.MatchString("p([a-z]+)ch", "peach")
	fmt.Println(match) //true

	r, _ := regexp.Compile("p([a-z]+)ch")

	fmt.Println(r.MatchString("peach"))                   //true
	fmt.Println(r.FindString("peach punch"))              //peach
	fmt.Println(r.FindStringIndex("peach punch"))         //[0 5]
	fmt.Println(r.FindStringSubmatch("peach punch"))      //[peach ea]
	fmt.Println(r.FindStringSubmatchIndex("peach punch")) //[0 5 1 3]
	fmt.Println(r.FindAllString("peach punch pinch", -1)) //[peach punch pinch]
	fmt.Println(r.FindAllStringSubmatchIndex(
		"peach punch pinch", -1)) //[[0 5 1 3] [6 11 7 9] [12 17 13 15]]
	fmt.Println(r.FindAllString("peach punch pinch", 2)) //[peach punch]
	fmt.Println(r.Match([]byte("peach")))                //true
	r = regexp.MustCompile("p([a-z]+)ch")
	fmt.Println(r) //p([a-z]+)ch

	fmt.Println(r.ReplaceAllString("a peach", "<fruit>")) //a <fruit>

	in := []byte("a peach")
	out := r.ReplaceAllFunc(in, bytes.ToUpper)
	fmt.Println(string(out)) //a PEACH
}

func jsonUsage() {

	type response1 struct {
		Page   int
		Fruits []string
	}

	type response2 struct {
		Page   int      `json:"page"`
		Fruits []string `json:"fruits"`
	}

	bolB, _ := json.Marshal(true)
	fmt.Println(string(bolB)) //true

	intB, _ := json.Marshal(1)
	fmt.Println(string(intB)) //1

	fltB, _ := json.Marshal(2.34)
	fmt.Println(string(fltB)) //2.34

	strB, _ := json.Marshal("gopher")
	fmt.Println(string(strB)) //"gopher"

	slcD := []string{"apple", "peach", "pear"}
	slcB, _ := json.Marshal(slcD)
	fmt.Println(string(slcB)) //["apple","peach","pear"]

	mapD := map[string]int{"apple": 5, "lettuce": 7}
	mapB, _ := json.Marshal(mapD)
	fmt.Println(string(mapB)) //{"apple":5,"lettuce":7}

	res1D := &response1{
		Page:   1,
		Fruits: []string{"apple", "peach", "pear"}}
	res1B, _ := json.Marshal(res1D)
	fmt.Println(string(res1B)) //{"Page":1,"Fruits":["apple","peach","pear"]}

	res2D := &response2{
		Page:   1,
		Fruits: []string{"apple", "peach", "pear"}}
	res2B, _ := json.Marshal(res2D)
	fmt.Println(string(res2B)) //{"page":1,"fruits":["apple","peach","pear"]}

	byt := []byte(`{"num":6.13,"strs":["a","b"]}`)

	var dat map[string]interface{}

	if err := json.Unmarshal(byt, &dat); err != nil {
		panic(err)
	}
	fmt.Println(dat) //map[num:6.13 strs:[a b]]

	num := dat["num"].(float64)
	fmt.Println(num) //6.13

	strs := dat["strs"].([]interface{})
	str1 := strs[0].(string)
	fmt.Println(str1) //a

	str := `{"page": 1, "fruits": ["apple", "peach"]}`
	res := response2{}
	json.Unmarshal([]byte(str), &res)
	fmt.Println(res)           //{1 [apple peach]}
	fmt.Println(res.Fruits[0]) //apple

	enc := json.NewEncoder(os.Stdout)
	d := map[string]int{"apple": 5, "lettuce": 7}
	enc.Encode(d) //{"apple":5,"lettuce":7}
}

// XML Usage --------------------------------------------------------------------------------------
type Plant struct {
	XMLName xml.Name `xml:"plant"`
	Id      int      `xml:"id,attr"`
	Name    string   `xml:"name"`
	Origin  []string `xml:"origin"`
}

func (p Plant) String() string {
	return fmt.Sprintf("Plant id=%v, name=%v, origin=%v",
		p.Id, p.Name, p.Origin)
}

func xmlUsage() {
	coffee := &Plant{Id: 27, Name: "Coffee"}
	coffee.Origin = []string{"Ethiopia", "Brazil"}

	out, _ := xml.MarshalIndent(coffee, " ", "  ")
	fmt.Println(string(out))
	/*
	 <plant id="27">
	   <name>Coffee</name>
	   <origin>Ethiopia</origin>
	   <origin>Brazil</origin>
	 </plant>
	*/

	fmt.Println(xml.Header + string(out))
	/*
		<?xml version="1.0" encoding="UTF-8"?>
		 <plant id="27">
		   <name>Coffee</name>
		   <origin>Ethiopia</origin>
		   <origin>Brazil</origin>
		 </plant>
	*/

	var p Plant
	if err := xml.Unmarshal(out, &p); err != nil {
		panic(err)
	}
	fmt.Println(p) //Plant id=27, name=Coffee, origin=[Ethiopia Brazil]

	tomato := &Plant{Id: 81, Name: "Tomato"}
	tomato.Origin = []string{"Mexico", "California"}

	type Nesting struct {
		XMLName xml.Name `xml:"nesting"`
		Plants  []*Plant `xml:"parent>child>plant"`
	}

	nesting := &Nesting{}
	nesting.Plants = []*Plant{coffee, tomato}

	out, _ = xml.MarshalIndent(nesting, " ", "  ")
	fmt.Println(string(out))
	/*
	 <nesting>
	   <parent>
	     <child>
	       <plant id="27">
	         <name>Coffee</name>
	         <origin>Ethiopia</origin>
	         <origin>Brazil</origin>
	       </plant>
	       <plant id="81">
	         <name>Tomato</name>
	         <origin>Mexico</origin>
	         <origin>California</origin>
	       </plant>
	     </child>
	   </parent>
	 </nesting>
	*/
}

func datetimeFormatting() {
	now := time.Now()
	p(now) //2012-10-31 15:50:13.793654 +0000 UTC

	then := time.Date(
		2009, 11, 17, 20, 34, 58, 651387237, time.UTC)
	p(then) //2009-11-17 20:34:58.651387237 +0000 UTC

	p(then.Year())       //2009
	p(then.Month())      //November
	p(then.Day())        //17
	p(then.Hour())       //20
	p(then.Minute())     //34
	p(then.Second())     //58
	p(then.Nanosecond()) //651387237
	p(then.Location())   //UTC

	p(then.Weekday()) //Tuesday

	p(then.Before(now)) //true
	p(then.After(now))  //false
	p(then.Equal(now))  //false

	diff := now.Sub(then)
	p(diff) //25891h15m15.142266763s

	p(diff.Hours())       //25891.25420618521
	p(diff.Minutes())     //1.5534752523711128e+06
	p(diff.Seconds())     //9.320851514226677e+07
	p(diff.Nanoseconds()) //93208515142266763

	p(then.Add(diff))  //2012-10-31 15:50:13.793654 +0000 UTC
	p(then.Add(-diff)) //2006-12-05 01:19:43.509120474 +0000 UTC
}

func unixtimeFormatting() {
	now := time.Now()
	secs := now.Unix()
	nanos := now.UnixNano()
	fmt.Println(now) //2012-10-31 16:13:58.292387 +0000 UTC

	millis := nanos / 1000000
	fmt.Println(secs)   //1351700038
	fmt.Println(millis) //1351700038292
	fmt.Println(nanos)  //1351700038292387000

	fmt.Println(time.Unix(secs, 0))  //2012-10-31 16:13:58 +0000 UTC
	fmt.Println(time.Unix(0, nanos)) //2012-10-31 16:13:58.292387 +0000 UTC
}

func timeParsing_formatting() {
	p := fmt.Println

	t := time.Now()
	p(t.Format(time.RFC3339)) //2014-04-15T18:00:15-07:00

	t1, e := time.Parse(
		time.RFC3339,
		"2012-11-01T22:08:41+00:00")
	p(t1) //2012-11-01 22:08:41 +0000 +0000

	p(t.Format("3:04PM"))                           //6:00PM
	p(t.Format("Mon Jan _2 15:04:05 2006"))         //Tue Apr 15 18:00:15 2014
	p(t.Format("2006-01-02T15:04:05.999999-07:00")) //2014-04-15T18:00:15.161182-07:00
	form := "3 04 PM"
	t2, e := time.Parse(form, "8 41 PM")
	p(t2) //0000-01-01 20:41:00 +0000 UTC

	fmt.Printf("%d-%02d-%02dT%02d:%02d:%02d-00:00\n",
		t.Year(), t.Month(), t.Day(),
		t.Hour(), t.Minute(), t.Second()) //2014-04-15T18:00:15-00:00

	ansic := "Mon Jan _2 15:04:05 2006"
	_, e = time.Parse(ansic, "8:41PM")
	p(e) //parsing time "8:41PM" as "Mon Jan _2 15:04:05 2006": ...
}

func randomNumberGeneration() {
	fmt.Print(rand.Intn(100), ",")
	fmt.Print(rand.Intn(100))
	fmt.Println() //81,87

	fmt.Println(rand.Float64()) //0.6645600532184904

	fmt.Print((rand.Float64()*5)+5, ",")
	fmt.Print((rand.Float64() * 5) + 5)
	fmt.Println() //7.123187485356329,8.434115364335547

	s1 := rand.NewSource(time.Now().UnixNano())
	r1 := rand.New(s1)

	fmt.Print(r1.Intn(100), ",")
	fmt.Print(r1.Intn(100))
	fmt.Println() //0,28

	s2 := rand.NewSource(42)
	r2 := rand.New(s2)
	fmt.Print(r2.Intn(100), ",")
	fmt.Print(r2.Intn(100))
	fmt.Println() //5,87
	s3 := rand.NewSource(42)
	r3 := rand.New(s3)
	fmt.Print(r3.Intn(100), ",")
	fmt.Print(r3.Intn(100))
	fmt.Println() //5,87
}

func numberParsing() {

	f, _ := strconv.ParseFloat("1.234", 64)
	fmt.Println(f) //1.234

	i, _ := strconv.ParseInt("123", 0, 64)
	fmt.Println(i) //123

	d, _ := strconv.ParseInt("0x1c8", 0, 64)
	fmt.Println(d) //456

	u, _ := strconv.ParseUint("789", 0, 64)
	fmt.Println(u) //789

	k, _ := strconv.Atoi("135")
	fmt.Println(k) //135

	_, e := strconv.Atoi("wat")
	fmt.Println(e) //strconv.ParseInt: parsing "wat": invalid syntax
}

func urlParsing() {
	ss := "postgres://user:pass@host.com:5432/path?k=v#f"

	u, err := url.Parse(ss)
	if err != nil {
		panic(err)
	}

	fmt.Println(u.Scheme) //postgres

	fmt.Println(u.User)            //user:pass
	fmt.Println(u.User.Username()) //user
	p, _ := u.User.Password()
	fmt.Println(p) //pass

	fmt.Println(u.Host) //host.com:5432
	host, port, _ := net.SplitHostPort(u.Host)
	fmt.Println(host) //host.com
	fmt.Println(port) //5432

	fmt.Println(u.Path)     ///path
	fmt.Println(u.Fragment) //f

	fmt.Println(u.RawQuery) //k=v
	m, _ := url.ParseQuery(u.RawQuery)
	fmt.Println(m)         //map[k:[v]]
	fmt.Println(m["k"][0]) //v
}

func sha1Generation() {
	ss := "sha1 this string"

	h := sha1.New()

	h.Write([]byte(ss))

	bs := h.Sum(nil)

	fmt.Println(ss)        //sha1 this string
	fmt.Printf("%x\n", bs) //cf23df2207d99a74fbe169e3eba035e633b65d94
}

func base64EncDec() {
	data := "abc123!?$*&()'-=@~"

	sEnc := b64.StdEncoding.EncodeToString([]byte(data))
	fmt.Println(sEnc) //YWJjMTIzIT8kKiYoKSctPUB+

	sDec, _ := b64.StdEncoding.DecodeString(sEnc)
	fmt.Println(string(sDec)) //	abc123!?$*&()'-=@~
	fmt.Println()             //

	uEnc := b64.URLEncoding.EncodeToString([]byte(data))
	fmt.Println(uEnc) //YWJjMTIzIT8kKiYoKSctPUB-
	uDec, _ := b64.URLEncoding.DecodeString(uEnc)
	fmt.Println(string(uDec)) //	abc123!?$*&()'-=@~
}

// FILE ---------------------------------------------------------------------------------------------------
func check(e error) {
	if e != nil {
		print("cant interact with file")
	}
}

func fileParsing() {
	// !!!!!!!!!!!!!!!!!!!!!!!!--------------------------------------!!!!!!!!!!!!!!!!!!!!!
	/*
		$ echo "hello" > /tmp/dat
		$ echo "go" >>   /tmp/dat
	*/

	dat, err := ioutil.ReadFile("/tmp/dat")
	check(err)
	if err != nil {
		return
	}
	fmt.Print(string(dat))
	/*
		hello
		go
	*/

	f, err := os.Open("/tmp/dat")
	check(err)
	if err != nil {
		return
	}

	b1 := make([]byte, 5)
	n1, err := f.Read(b1)
	check(err)
	if err != nil {
		return
	}
	fmt.Printf("%d bytes: %s\n", n1, string(b1[:n1])) //	5 bytes: hello

	o2, err := f.Seek(6, 0)
	check(err)
	if err != nil {
		return
	}
	b2 := make([]byte, 2)
	n2, err := f.Read(b2)
	check(err)
	if err != nil {
		return
	}
	fmt.Printf("%d bytes @ %d: ", n2, o2) //  2 bytes @ 6: go
	fmt.Printf("%v\n", string(b2[:n2]))

	o3, err := f.Seek(6, 0)
	check(err)
	if err != nil {
		return
	}
	b3 := make([]byte, 2)
	n3, err := io.ReadAtLeast(f, b3, 2)
	check(err)
	if err != nil {
		return
	}
	fmt.Printf("%d bytes @ %d: %s\n", n3, o3, string(b3)) //	2 bytes @ 6: go
	_, err = f.Seek(0, 0)
	check(err)
	if err != nil {
		return
	}

	r4 := bufio.NewReader(f)
	b4, err := r4.Peek(5)
	check(err)
	if err != nil {
		return
	}
	fmt.Printf("5 bytes: %s\n", string(b4)) //	5 bytes: hello

	f.Close()
}

func fileWriting() {

	d1 := []byte("hello\ngo\n")
	err := ioutil.WriteFile("/tmp/dat1", d1, 0644)
	check(err)
	if err != nil {
		return
	}

	f, err := os.Create("/tmp/dat2")
	check(err)
	if err != nil {
		return
	}

	defer f.Close()

	d2 := []byte{115, 111, 109, 101, 10}
	n2, err := f.Write(d2)
	check(err)
	if err != nil {
		return
	}
	fmt.Printf("wrote %d bytes\n", n2)

	n3, err := f.WriteString("writes\n")
	check(err)
	if err != nil {
		return
	}
	fmt.Printf("wrote %d bytes\n", n3)

	f.Sync()
	/* dat1
	hello
	go
	*/

	w := bufio.NewWriter(f)
	n4, err := w.WriteString("buffered\n")
	check(err)
	if err != nil {
		return
	}
	fmt.Printf("wrote %d bytes\n", n4)

	w.Flush()
	/* dat2
	some
	writes
	buffered
	*/
}

func filePathes() {
	p := filepath.Join("dir1", "dir2", "filename")
	fmt.Println("p:", p) //p: dir1/dir2/filename

	fmt.Println(filepath.Join("dir1//", "filename"))       //dir1/filename
	fmt.Println(filepath.Join("dir1/../dir1", "filename")) //dir1/filename

	fmt.Println("Dir(p):", filepath.Dir(p))   //Dir(p): dir1/dir2
	fmt.Println("Base(p):", filepath.Base(p)) //Base(p): filename

	fmt.Println(filepath.IsAbs("dir/file"))  //false
	fmt.Println(filepath.IsAbs("/dir/file")) //true

	filename := "config.json"

	ext := filepath.Ext(filename)
	fmt.Println(ext) //.json

	fmt.Println(s.TrimSuffix(filename, ext)) //config

	rel, err := filepath.Rel("a/b", "a/b/t/file")
	if err != nil {
		panic(err)
	}
	fmt.Println(rel) //t/file

	rel, err = filepath.Rel("a/b", "a/c/t/file")
	if err != nil {
		panic(err)
	}
	fmt.Println(rel) //../c/t/file
}

func tempFileDir() {

	f, err := ioutil.TempFile("", "sample")
	check(err)
	if err != nil {
		return
	}

	fmt.Println("Temp file name:", f.Name())

	defer os.Remove(f.Name())

	_, err = f.Write([]byte{1, 2, 3, 4})
	check(err)
	if err != nil {
		return
	}

	dname, err := ioutil.TempDir("", "sampledir")
	check(err)
	if err != nil {
		return
	}
	fmt.Println("Temp dir name:", dname)

	defer os.RemoveAll(dname)

	fname := filepath.Join(dname, "file1")
	err = ioutil.WriteFile(fname, []byte{1, 2}, 0666)
	check(err)
	if err != nil {
		return
	}
}

func lineFilters() {

	scanner := bufio.NewScanner(os.Stdin)

	for scanner.Scan() {

		ucl := s.ToUpper(scanner.Text())

		fmt.Println(ucl)
	}

	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		os.Exit(1)
	}
}
