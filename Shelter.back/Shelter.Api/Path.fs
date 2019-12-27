module Path

type IntPath = PrintfFormat<(int -> string), unit, string, string, int>

let home = "/"

module Gems = 
    let overview = "/api/gems"
    let searchForGems = "/api/gems/search"
    let creation = "/api/gems"
    let tests = "/api/tests"
    let details : IntPath = "/api/gems/%d"

