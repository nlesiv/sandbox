/**
In this exercise, we want to implement the backend of a spreadsheet application.
That is, we need a library that lets us set(row, column, value) and get(row, column) the contents of the spreadsheet.
We'll start by implementing only basic functionality like getting and setting strings,
but we'll try to work our way up to supporting formulas with dependencies on other cells.
*/
let sheet = {};

isNumeric = (value) => {
    return true;
}
set =(row, column, value) => {
    if(!sheet[row]) {
        sheet[row] = {};
    }

    sheet[row][column] = value;
    
}

set('AA', '2090', 'test')

console.log(sheet);

get = (row, column)  => {
    let value = sheet && sheet[row] && sheet[row][column]

    if(!value && value !== 0) {
        return null
    }

    if(typeof value == 'string' && value.length) {
        if(value[0] === '=') {
            let formula = value.substring(1);

            if(formula && formula.length) {
                let parts = formula.split("+")

                if(parts && parts.length >= 2) {

                    let a = getValue(parts[0]);
                    let b = getValue(parts[1]);

                    if(isNumeric(a) && isNumeric(b)) {
                        return a + b;
                    }

                    



                    return null;
                }
            }
        }
    }

    return value;
}

getValue = (cell) =>  {
    let value;
    if(isCellReference(cell)) {

    }

    return parseFloat(value);

}

isCellReference = (value) => {

}

console.log(get('BB', '22'));
console.log(get('AA', '2090'));

set('AA', '2090', 'another test')
console.log(get('AA', '2090'));

set('AA', '2091', "=1+3")
console.log(get('AA', '2091'));

set('A', '1', "2")
set('B', '1', "4")
set('C', '1', "=A1+B1")

// Usage:
// set("A", 1, "Hello");
// get("A", 1); // => "Hello"