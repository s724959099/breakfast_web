/**
 * Created by Admin on 2017/11/18.
 */
Array.prototype.in = function (val) {
  return this.includes(val)
}

Array.prototype.not_in = function (val) {
  return !this.in(val)

}

Array.prototype.append = function (...val) {
  return this.push(...val)

}

Array.prototype.remove = function (val) {
  if (Array.isArray(val)) {
    for (let item of val) {
      this.remove(item)
    }
    return this
  }
  let index = this.indexOf(val)
  if (index !== -1)
    this.splice(index, 1)
  return this

}
Array.prototype.remove_by_index =function (index) {
  if (index !== -1)
    this.splice(index, 1)
  return this

}

Array.prototype.change = function (old_val, new_val) {
  let index = this.indexOf(old_val)
  if (index !== -1)
    this[index] = new_val
  return this

}

Array.prototype.change_obj_with_key = function (key, val,new_obj) {
  return this.map((obj) => {
    if(obj[key]===val){
      return new_obj
    }else{
      return obj
    }
  })
}


Array.prototype.remove_obj_with_key = function (key, val) {
  return this.filter((obj) => {
    return obj[key] !== val
  })
}
Array.prototype.is_in_obj_with_key = function (key, val) {
  let data = this.filter((obj) => {
    return obj[key] === val
  })
  if(data.length){
    return true
  }else{
    return false
  }
}

Array.prototype.in_obj_with_key = function (key, val) {
  let data = this.filter((obj) => {
    return obj[key] === val
  })
  return data
}





Array.init_data = function (num, value) {
  return Array.from(new Array(num).keys()).map((val) => {
    if (typeof value === "function") {
      return value()
    } else {
      return value
    }

  })
}


window.range = (num, start = 0) => {
  return Array.from(new Array(num).keys()).map((val) => {
    return val + start
  })
}



