var board,
    game = new Chess();

/*The "AI" part starts here */
var isMaximisingPlayer = true;
var teamVS = /^b/;
var minimaxRoot =function(depth, game, isMaximisingPlayer) {    // hàm bắt đàu chạy 

    var newGameMoves = game.ugly_moves();                       // lấy tập tất cả các nước có thể đi
    var bestMove = -9999;
    var bestMoveFound;
    if (isMaximisingPlayer) {

        for(var i = 0; i < newGameMoves.length; i++) {
            var newGameMove = newGameMoves[i]
            game.ugly_move(newGameMove);
            var value = minimax(depth - 1, game, -10000, 10000, !isMaximisingPlayer);
            game.undo();
            if(value >= bestMove) {
                bestMove = value;
                bestMoveFound = newGameMove;
            }
        }
    }
    else{
        bestMove = 9999;
        for(var i = 0; i < newGameMoves.length; i++) {
            var newGameMove = newGameMoves[i]
            game.ugly_move(newGameMove);
            var value = minimax(depth - 1, game, -10000, 10000, !isMaximisingPlayer);
            game.undo();
            if(value <= bestMove) {
                bestMove = value;
                bestMoveFound = newGameMove;
            }
        }
    }
    return bestMoveFound;
};

var minimax = function (depth, game, alpha, beta, isMaximisingPlayer) { // giải thuật cắt tỉa anpha beta
    positionCount++;                            // mỗi lần gọi tăng lên 1. Để đếm số nước đi
    if (depth === 0) {
        return -evaluateBoard(game.board());
    }	

    var newGameMoves = game.ugly_moves();       //di chuyển bừa một nước

    if (isMaximisingPlayer) {
        var bestMove = -9999;
        for (var i = 0; i < newGameMoves.length; i++) {
            game.ugly_move(newGameMoves[i]);
            bestMove = Math.max(bestMove, minimax(depth - 1, game, alpha, beta, !isMaximisingPlayer));  // rồi tính
            // điểm mước đi đó
            game.undo();
            alpha = Math.max(alpha, bestMove);
            if (beta <= alpha) {
                return bestMove;
            }
        }
        return bestMove;
    } else {
        var bestMove = 9999;
        for (var i = 0; i < newGameMoves.length; i++) {
            game.ugly_move(newGameMoves[i]);
            bestMove = Math.min(bestMove, minimax(depth - 1, game, alpha, beta, !isMaximisingPlayer));
            game.undo();
            beta = Math.min(beta, bestMove);
            if (beta <= alpha) {
                return bestMove;
            }
        }
        return bestMove;
    }
};

var evaluateBoard = function (board) {      // tính điểm của thế cờ
    var totalEvaluation = 0;
    for (var i = 0; i < 8; i++) {
        for (var j = 0; j < 8; j++) {
            totalEvaluation = totalEvaluation + getPieceValue(board[i][j], i ,j);
        }
    }
    return totalEvaluation;
};

var reverseArray = function(array) {
    return array.slice().reverse();
};

var rootpawnEvalWhite =                                     // tốt
    [
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
    ];

var rootpawnEvalBlack = reverseArray(rootpawnEvalWhite);        // đảo ngược lại ma trận

var knightEval =                                        // mã
    [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
        [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
        [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
        [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
        [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
        [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
    ];

var rootbishopEvalWhite = [                                 // tượng
    [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
    [ -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
    [ -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
    [ -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
    [ -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
    [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
];

var rootbishopEvalBlack = reverseArray(rootbishopEvalWhite);

var rootrookEvalWhite = [                                   // xe
    [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [  0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
];

var rootrookEvalBlack = reverseArray(rootrookEvalWhite);

var evalQueen = [                                       // hậu
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
];

var rootkingEvalWhite = [                                   // vua

    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
    [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]
];

var rootkingEvalBlack = reverseArray(rootkingEvalWhite);




var getPieceValue = function (piece, x, y) {    // tính điểm của từng con cờ
    if (piece === null) {
        return 0;
    }
    var getAbsoluteValue = function (piece, isWhite, x ,y) {
        if (piece.type === 'p') {               // điểm quân tốt
            return 10 + ( isWhite ? pawnEvalWhite[y][x] : pawnEvalBlack[y][x] );
        } else if (piece.type === 'r') {        // quân xe
            return 50 + ( isWhite ? rookEvalWhite[y][x] : rookEvalBlack[y][x] );
        } else if (piece.type === 'n') {        // quân mã
            return 40 + knightEval[y][x];
        } else if (piece.type === 'b') {        // tịnh
            return 30 + ( isWhite ? bishopEvalWhite[y][x] : bishopEvalBlack[y][x] );
        } else if (piece.type === 'q') {        // hậu
            return 90 + evalQueen[y][x];    
        } else if (piece.type === 'k') {        // vua
            return 900 + ( isWhite ? kingEvalWhite[y][x] : kingEvalBlack[y][x] );
        }
        throw "Unknown piece type: " + piece.type;
    };

    var absoluteValue = getAbsoluteValue(piece, piece.color === 'w', x ,y);	
    // kiểm tra xem có phải team mình ko
        // var absoluteValue = getAbsoluteValue(piece, piece.color === team, x ,y);
    return piece.color === 'w' ? absoluteValue : -absoluteValue;
        // return piece.color === team ? absoluteValue : -absoluteValue;

};


/* board visualization and games state handling */

var onDragStart = function (source, piece, position, orientation) {    // keo chuột
    if (game.in_checkmate() === true || game.in_draw() === true ||
        // piece.search(/^b/) !== -1) {
       	piece.search(teamVS) !== -1) {
        console.log("teamVS on Drag   ",teamVS);
        return false;
    }
};

var makeBestMove = function () {        // di chuyển cờ theo nước đi tốt nhất
    var bestMove = getBestMove(game);   // tìm nước đi tốt nhất //201
    game.ugly_move(bestMove);
    board.position(game.fen());
    renderMoveHistory(game.history());
    if (game.game_over()) {
        alert('Game over');
    }
};


var positionCount;
var getBestMove = function (game) {                 // tìm mước đi tốt nhất
    if (game.game_over()) {
        alert('Game over');
    }

    positionCount = 0;                              // só nước đi giải thuật đã dự đoán
    var depth = parseInt($('#search-depth').find(':selected').text());

    var d = new Date().getTime();
    // var bestMove = minimaxRoot(depth, game, true);  //giải thuật minimax  // 25
    var bestMove = minimaxRoot(depth, game, isMaximisingPlayer);
    var d2 = new Date().getTime();
    var moveTime = (d2 - d);
    var positionsPerS = ( positionCount * 1000 / moveTime);

    $('#position-count').text(positionCount);
    $('#time').text(moveTime/1000 + 's');
    $('#positions-per-s').text(positionsPerS);
    return bestMove;
};

var renderMoveHistory = function (moves) {      // hiển thị danh sách các nước đi
    var historyElement = $('#move-history').empty();
    historyElement.empty();
    for (var i = 0; i < moves.length; i = i + 2) {
        historyElement.append('<span>' + moves[i] + ' ' + ( moves[i + 1] ? moves[i + 1] : ' ') + '</span><br>')
    }
    historyElement.scrollTop(historyElement[0].scrollHeight);

};

var onDrop = function (source, target) {    // nhấp chuột
                                            // kiểm tra tính hợp lệ của nước đi để đi
    console.log("isWhite  ",isMaximisingPlayer);
    console.log("teamVS  ",teamVS);

    var move = game.move({
        from: source,
        to: target,
        promotion: 'q'
    });

    console.log("onDrop move  "+ move);

    removeGreySquares();
    if (move === null) {                    // nước đi không hợp lệ thì quay lại
        return 'snapback';
    }

    renderMoveHistory(game.history());      // hợp lệ thì đi và ghi nó vào lịch sử
    window.setTimeout(makeBestMove, 500);   // chạy giải thuật AI
};

var onSnapEnd = function () {
    board.position(game.fen());
};

var onMouseoverSquare = function(square, piece) {   // chuột qua con cờ
    // console.log("onMouseoverSquare square  "+ square);

    var moves = game.moves({
        square: square,
        verbose: true
    });

    if (moves.length === 0) return;

    greySquare(square);

    for (var i = 0; i < moves.length; i++) {
        greySquare(moves[i].to);
    }
};

var onMouseoutSquare = function(square, piece) {
    removeGreySquares();
};

var removeGreySquares = function() {
    $('#board .square-55d63').css('background', '');
};

var greySquare = function(square) {             // tạo phần màu nâu những nước đi hợp lệ
    var squareEl = $('#board .square-' + square);

    var background = '#a9a9a9';
    if (squareEl.hasClass('black-3c85d') === true) {
        background = '#696969';
    }

    squareEl.css('background', background);
};

var cfg = {
    draggable: true,
    // position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onMouseoutSquare: onMouseoutSquare,
    onMouseoverSquare: onMouseoverSquare,
    onSnapEnd: onSnapEnd,
    sparePieces: true,
    pieceTheme:"img/chesspieces/wikipedia/{piece}.png"
    // snapbackSpeed: 500,
  	// snapSpeed: 100,
};

board = ChessBoard('board', cfg);



$('#newgame').on('click', function() {
    var theme = document.getElementById("pieceTheme");
    var themepiece = parseInt(theme.options[theme.selectedIndex].value);

    if(themepiece==1){
        cfg.pieceTheme = 'img/chesspieces/wikipedia/{piece}.png';
        console.log("pieceTheme    :",cfg.pieceTheme);
    }
    else if(themepiece==2){
        cfg.pieceTheme = 'img/chesspieces/theme1/{piece}.png';
        console.log("pieceTheme    :",cfg.pieceTheme);
    }
    else if(themepiece==3){
        cfg.pieceTheme = 'img/chesspieces/theme2/{piece}.png';
        console.log("pieceTheme    :",cfg.pieceTheme);
    }


    var e = document.getElementById("select-team");
    var team = parseInt(e.options[e.selectedIndex].value);
    console.log("team    :",team);


    if(team==1){



        game.clear();
        board.clear();
        game.load('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');
        // board.position(game.fen());
        if(!isMaximisingPlayer){
            board.flip();
        }
        board.start(); 
        isMaximisingPlayer = true;
        teamVS = /^b/;  

        pawnEvalWhite = rootpawnEvalWhite;
        pawnEvalBlack = rootpawnEvalBlack;

        rookEvalWhite = rootrookEvalWhite;
        rookEvalBlack = rootrookEvalBlack;

        bishopEvalWhite = rootbishopEvalWhite;
        bishopEvalBlack = rootbishopEvalBlack;

        kingEvalWhite = rootkingEvalWhite;
        kingEvalBlack = rootkingEvalBlack;


        $('#move-history').empty();
    }    
    else{



        game.clear();
        board.clear();
        game.load('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');
        // board.position(game.fen());
        // board.flip();
        if(isMaximisingPlayer){
            board.flip();
        }
        game.load(board.fen());
        board.start(); 


        isMaximisingPlayer = false;
        teamVS = /^w/;


        pawnEvalWhite = rootpawnEvalBlack;
        pawnEvalBlack = rootpawnEvalWhite;

        rookEvalWhite = rootrookEvalBlack;
        rookEvalBlack = rootrookEvalWhite;

        bishopEvalWhite = rootbishopEvalBlack;
        bishopEvalBlack = rootbishopEvalWhite;

        kingEvalWhite = rootkingEvalBlack;
        kingEvalBlack = rootkingEvalWhite;
        $('#move-history').empty();
    }


    if(isMaximisingPlayer==false){
        console.log("make best Move");
        window.setTimeout(makeBestMove, 500);   // chạy giải thuật AI
    }   
	console.log("new game");
});
$('#back').on('click', function() {
  	game.undo();
	board.position(game.fen());
	console.log("back back");
});



/*
$('#changeteam').on('click', function() {
  	board.flip();
  	game.load(board.fen());
    var temp;
    
    temp = pawnEvalWhite;
    pawnEvalWhite = pawnEvalBlack;
    pawnEvalBlack = temp;

    temp = rookEvalWhite;
    rookEvalWhite = rookEvalBlack;
    rookEvalBlack = temp;

    temp = bishopEvalWhite;
    bishopEvalWhite = bishopEvalBlack;
    bishopEvalBlack = temp;

    temp = kingEvalWhite;
    kingEvalWhite = kingEvalBlack;
    kingEvalBlack = temp;

  	isMaximisingPlayer = !isMaximisingPlayer;
  	if(isMaximisingPlayer){
  		teamVS = /^b/;
  	}
  	else{
  		  teamVS = /^w/;
  	}
});
*/