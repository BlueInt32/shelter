module Path

type IntPath = PrintfFormat<(int -> string), unit, string, string, int>

let home = "/"

module Gems = 
    let overview = "/api/gems"
    let creation = "/api/gems"
    let details : IntPath = "/api/gems/%d"

