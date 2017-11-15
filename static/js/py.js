/**
 * Created by Admin on 2017/9/21.
 */
function len(obj) {
  return obj.length
}
window.len = len
function* zip(arr1, arr2) {
  let min = Math.min(
    len(arr1),
    len(arr2)
  )
  for (let i = 0; i < min; i++) {
    yield [arr1[i], arr2[i]]
  }
}
window.zip = zip

function dict_get(obj, key = null, default_data = null) {
  if (obj === null || obj===undefined) {
    return default_data
  }
  return (obj[key] !== undefined) ? obj[key] : default_data
}
window.dict_get = dict_get

function dict(obj = {}) {
  const prevent_show = ["setdefault", "get", "has_key", "keys", "values", "items"]
  let dict_obj = {
    setdefault(key, default_val = null){
      if (!this.has_key(key)) {
        this[key] = default_val
      }
      return this[key]
    },
    get(key, default_val = null){
      if (this.has_key(key)) {
        return this[key]
      } else {
        return default_val
      }
    },
    has_key(key){
      if (prevent_show.in(key))
        return false
      return key in this

    },
    keys(){
      let result = []
      for (let key of Object.keys(this)) {
        if (this.has_key(key))
          result.append(key)
      }
      return result
    },
    values(){
      let result = []
      for (let key of this.keys()) {
        result.append(this[key])
      }
      return result
    },
    items(){
      return zip(this.keys(), this.values())
    },
  }
  return Object.assign(obj, dict_obj)
}
window.dict = dict

window.py = {
  __name__(val){
    return Object.keys(val)[0]
  },
}
function print(...val) {
  console.log(...val)
}
window.print = print
