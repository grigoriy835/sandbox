import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';


function Board(props) {
    return (
        <div>
            {
                props.square.map((line, i) => {
                    return (
                        <div key={i} className="board-row">
                            {line.map((col, j) => {
                                let isItWon = props.winner && props.winner[1].includes(`${i}-${j}`)
                                return (
                                    <button key={`${i}${j}`} className={isItWon?"square won-square":"square"} onClick={() => props.onClick(i, j)}>
                                        {props.square[i][j]}
                                    </button>
                                )
                            })}
                        </div>
                    )

                })
            }
        </div>
    );
}

class Game extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            replaying: false,
            history: [
                {
                    squares: Array(this.props.high).fill(null).map(() => {
                        return Array(this.props.width).fill(null);
                    }),
                    move: [null, null, null]
                }
            ],
            stepNumber: 0,
            xIsNext: true
        };
    }

    async replay() {
        if (this.state.replaying) {
            this.state.replaying = false;
            return;
        }
        this.state.replaying = true;
        for (const step of this.state.history) {
            const s_number = this.state.history.indexOf(step);
            if (!this.state.replaying) return;
            if (s_number === this.state.history.length - 1) this.state.replaying = false;
            this.setState({
                stepNumber: s_number,
                xIsNext: (step % 2) === 0
            })
            await new Promise(r => setTimeout(r, 500));
        }
    }

    handleClick(i, j) {
        const history = this.state.history.slice(0, this.state.stepNumber + 1);
        const current = history[history.length - 1];
        const squares = current.squares.map(line => {return line.slice()});
        if (calculateWinner(squares, this.props.winRowSize) || squares[i][j] || this.state.replaying) {
            return;
        }
        squares[i][j] = this.state.xIsNext ? "X" : "O";
        this.setState({
            history: history.concat([
                {
                    squares: squares,
                    move: [squares[i][j], i, j],
                }
            ]),
            stepNumber: history.length,
            xIsNext: !this.state.xIsNext
        });
    }

    jumpTo(step) {
        this.setState({
            stepNumber: step,
            xIsNext: (step % 2) === 0
        });
    }

    render() {
        const history = this.state.history;
        const current = history[this.state.stepNumber];
        const winner = calculateWinner(current.squares, this.props.winRowSize);

        const moves = history.map((step, move_num) => {
            const desc = move_num ?
                'move #' + move_num :
                'game start';
            return (
                <li key={move_num}>
                    <button
                        className={move_num === this.state.stepNumber ? 'selected-move' : ''}
                        onClick={() => this.jumpTo(move_num)}
                    >{desc}</button>
                    <span className="move-note">{move_num ? step.move[0] + ' ' + step.move[1] + '-' + step.move[2] : ''}</span>
                </li>
            );
        });

        let status;
        if (winner) {
            status = "Winner: " + winner[0];
        } else {
            status = "Next player: " + (this.state.xIsNext ? "X" : "O");
        }

        return (
            <div className="game">
                <div className="game-board">
                    <Board
                        square={current.squares}
                        winner={winner}
                        onClick={(i, j) => this.handleClick(i, j)}
                    />
                </div>
                <div className="game-info">
                    <div>{status}</div>
                    <ol>{moves}</ol>
                </div>
                <div className="replay">
                    <button onClick={() => this.replay()}>{this.state.replaying ? 'stop replay' : 'replay'}</button>
                </div>
            </div>
        );
    }
}

// ========================================

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Game high={40} width={57} winRowSize={5}/>);

function calculateWinner(squares, winRowSize) {
    function diagonalCheck(squares, i, j) {
        if (i < winRowSize - 1) return null;
        if (j > winRowSize - 1) {
            let chain = [squares[i][j], [`${i}-${j}`]]
            for (let c = 1; c < winRowSize; c++) {
                if (squares[i][j] !== squares[i - c][j - c]) break;
                chain[1].push(`${i - c}-${j - c}`);
            }
            if (chain[1].length >= winRowSize) return chain;

        }
        if (j < squares[0].length - winRowSize + 1) {
            let chain = [squares[i][j], [`${i}-${j}`]]
            for (let c = 1; c < winRowSize; c++) {
                if (squares[i][j] !== squares[i - c][j + c]) break;
                chain[1].push(`${i - c}-${j + c}`);
            }
            if (chain[1].length >= winRowSize) return chain;

        }
        return null;
    }

    for (let i = 0; i < squares.length; i++) {
        let lineCheck = [null, []];
        for (let j = 0; j < squares[0].length; j++) {
            if (squares[i][j]) {
                let diagonal = diagonalCheck(squares, i, j);
                if (diagonal) return diagonal;
                if (squares[i][j] === lineCheck[0]) {
                    lineCheck[1].push(`${i}-${j}`)
                } else {
                    lineCheck = [squares[i][j], [`${i}-${j}`]];
                }
                if (lineCheck[1].length >= winRowSize) return lineCheck;

            } else {
                lineCheck = [null, []];
            }
        }
    }
    for (let i = 0; i < squares[0].length; i++) {
        let colCheck = [null, []];
        for (let j = 0; j < squares.length; j++) {

            if (squares[j][i]) {
                if (squares[j][i] === colCheck[0]) {
                    colCheck[1].push(`${j}-${i}`);
                } else {
                    colCheck = [squares[j][i], [`${j}-${i}`]];
                }
                if (colCheck[1].length >= winRowSize) return colCheck;

            } else {
                colCheck = [null, []];
            }
        }
    }

    return null;
}

