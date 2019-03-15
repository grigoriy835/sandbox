const _ = require('underscore');

let tt = [];

function check_field(field)
{
    let arrays = [];

    _.each(field, function (line) {
        arrays.push(line)
    });

    _.each(range(9, 1), function (index) {
        let column = [];
        _.each(field, function (line) {
            column.push(line[index])
        });
        arrays.push(column);
    });

    _.each([0,1,2], function (cube_x) {
        _.each([0,1,2], function (cube_y) {
            let cube = [];
            if (typeof field[cube_x*3] === 'array') {
                cube.push(field[cube_x*3][cube_y*3]);
                cube.push(field[cube_x*3][cube_y*3+1]);
                cube.push(field[cube_x*3][cube_y*3+2]);
            }
            if (typeof field[cube_x*3+1] === 'array') {
                cube.push(field[cube_x*3+1][cube_y*3]);
                cube.push(field[cube_x*3+1][cube_y*3+1]);
                cube.push(field[cube_x*3+1][cube_y*3+2]);
            }
            if (typeof field[cube_x*3+2] === 'array') {
                cube.push(field[cube_x*3+2][cube_y*3]);
                cube.push(field[cube_x*3+2][cube_y*3+1]);
                cube.push(field[cube_x*3+2][cube_y*3+2]);
            }

            arrays.push(cube)
        });
    });

    _.each(arrays, function (arr) {

    });

    return true
}

function range(size, startAt = 0) {
    return [...Array(size).keys()].map(i => i + startAt);
}
