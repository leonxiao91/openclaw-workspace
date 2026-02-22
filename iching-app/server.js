const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// 64卦数据
const hexagrams = {
    1: { name: '乾', latin: 'Qian', english: 'Creative', gua: '�乾', meaning: '象征天，创始万物，纯阳刚健。代表创始、力量、行动力。', judgment: '元亨利贞', judgmentMeaning: '大亨通利于正定' },
    2: { name: '坤', latin: 'Kun', english: 'Receptive', gua: '䷁', meaning: '象征地，顺从承载，万物生长。代表柔顺、包容、大地之德。', judgment: '元亨利牝马之贞', judgmentMeaning: '像母马一样柔顺而有益' },
    3: { name: '屯', latin: 'Zhun', english: 'Difficulty', gua: '䷬', meaning: '象征初生，困难重重但蕴含生机。代表事物萌芽期的艰难。', judgment: '元亨利贞勿用有攸往利建侯', judgmentMeaning: '利于建立侯爵之位' },
    4: { name: '蒙', latin: 'Meng', english: 'Youth', gua: '䷃', meaning: '象征蒙昧，教育启蒙之时。代表需要学习和指导。', judgment: '亨匪我求童蒙童蒙求我', judgmentMeaning: '不是我去求蒙童，而是蒙童来求我' },
    5: { name: '需', latin: 'Xu', english: 'Waiting', gua: '䷄', meaning: '象征等待，时机未到需耐心。代表蓄势待发。', judgment: '有孚光亨贞吉利涉大川', judgmentMeaning: '心怀诚信则光大亨通' },
    6: { name: '讼', latin: 'Song', english: 'Conflict', gua: '䷅', meaning: '象征争讼，是非冲突。代表有纠纷需要解决。', judgment: '有孚窒惕中吉终凶', judgmentMeaning: '诚信受阻，警惕则中间吉祥' },
    7: { name: '师', latin: 'Shi', english: 'Army', gua: '䷇', meaning: '象征军队，代表战争或领导众人。', judgment: '贞丈人吉无咎', judgmentMeaning: '正固则有老人吉祥' },
    8: { name: '比', latin: 'Bi', english: 'Alliance', gua: '䷇', meaning: '象征亲比，相亲相辅。代表合作与联盟。', judgment: '吉原筮元永贞无咎', judgmentMeaning: '应当最初的卜筮，保持正固' },
    9: { name: '小畜', latin: 'Xiao Chu', english: 'Small Taming', gua: '䷈', meaning: '象征小有积蓄，力量不足。代表渐进积累。', judgment: '亨密云不雨自我西郊', judgmentMeaning: '云多而不雨，从我西郊升起' },
    10: { name: '履', latin: 'Lu', english: 'Treading', gua: '䷉', meaning: '象征实践，踩着老虎尾巴走。代表谨慎行事。', judgment: '履虎尾不咥人亨', judgmentMeaning: '踩老虎尾巴不被咬，亨通' },
    11: { name: '泰', latin: 'Tai', english: 'Peace', gua: '䷊', meaning: '象征通泰，天地相交。代表太平盛世。', judgment: '小往大来吉亨', judgmentMeaning: '小的往而大的来，吉祥亨通' },
    12: { name: '否', latin: 'Pi', english: 'Blockage', gua: '䷋', meaning: '象征闭塞，天地不交。代表困难时期。', judgment: '否之匪人不利君子贞', judgmentMeaning: '闭塞不是人造成的' },
    13: { name: '同人', latin: 'Tong Ren', english: 'Fellowship', gua: '䷌', meaning: '象征同人，与人和同。代表合作与同心。', judgment: '同人于野亨利涉大川', judgmentMeaning: '在田野与人和同，利于渡过大河' },
    14: { name: '大有', latin: 'Da You', english: 'Great Possession', gua: '䷍', meaning: '象征大有，所有丰有。代表大获所有。', judgment: '元亨', judgmentMeaning: '大亨通' },
    15: { name: '谦', latin: 'Qian', english: 'Modesty', gua: '䷎', meaning: '象征谦逊，地山谦。代表君子有终。', judgment: '亨君子有终', judgmentMeaning: '亨通，君子有好的结果' },
    16: { name: '豫', latin: 'Yu', english: 'Enthusiasm', gua: '䷏', meaning: '象征愉悦，雷地豫。代表欢乐与预备。', judgment: '利建侯行师', judgmentMeaning: '利于封侯建军' },
    17: { name: '随', latin: 'Sui', english: 'Following', gua: '䷐', meaning: '象征随从，随和而从。代表顺从与随行。', judgment: '元亨利贞无咎', judgmentMeaning: '大亨通利于正固没有灾祸' },
    18: { name: '蛊', latin: 'Gu', english: 'Decay', gua: '䷑', meaning: '象征腐败，事物败坏。代表需要整饬。', judgment: '元亨利涉大川先甲三日后甲三日', judgmentMeaning: '大亨通，利于渡过大河' },
    19: { name: '临', latin: 'Lin', english: 'Approach', gua: '䷒', meaning: '象征来临，地泽临。代表王者降临。', judgment: '元亨利贞至于八月有凶', judgmentMeaning: '大亨通利于正固，到八月有凶险' },
    20: { name: '观', latin: 'Guan', english: 'Contemplation', gua: '䷓', meaning: '象征观察，风地观。代表审视与展示。', judgment: '盥而不荐有孚颙若', judgmentMeaning: '洗手而不献祭，心怀诚信' },
    21: { name: '噬嗑', latin: 'Shi Ke', english: 'Biting', gua: '䷔', meaning: '象征噬磕，咬合食物。代表法律与刑罚。', judgment: '亨利用狱', judgmentMeaning: '亨通，利于用刑' },
    22: { name: '贲', latin: 'Bi', english: 'Adornment', gua: '䷕', meaning: '象征文饰，山火贲。代表美化与装饰。', judgment: '亨小利有攸往', judgmentMeaning: '亨通，稍微有利' },
    23: { name: '剥', latin: 'Bo', english: 'Stripping', gua: '䷖', meaning: '象征剥落，山地剥。代表衰退与小人得势。', judgment: '不利有攸往', judgmentMeaning: '不利于前往' },
    24: { name: '复', latin: 'Fu', english: 'Return', gua: '䷗', meaning: '象征复返，地雷复。代表阳气回复。', judgment: '亨出入无疾朋来无咎反复其道七日来复', judgmentMeaning: '亨通，出入无病，朋友来无灾' },
    25: { name: '无妄', latin: 'Wu Wang', english: 'Innocence', gua: '䷘', meaning: '象征无妄，天雷无妄。代表不妄为。', judgment: '元亨利贞其匪正有眚不利有攸往', judgmentMeaning: '如果不正就有灾祸' },
    26: { name: '大畜', latin: 'Da Chu', english: 'Great Taming', gua: '䷙', meaning: '象征大畜，山天大畜。代表大为畜积。', judgment: '利贞不家食吉利涉大川', judgmentMeaning: '利于正固，不在家吃饭吉祥' },
    27: { name: '颐', latin: 'Yi', english: 'Nourishment', gua: '䷚', meaning: '象征颐养，山雷颐。代表养身与养德。', judgment: '贞吉观颐自求口实', judgmentMeaning: '正固吉祥，观察颐养之道' },
    28: { name: '大过', latin: 'Da Guo', english: 'Great Exceeding', gua: '䷛', meaning: '象征大过，泽风大过。代表过度与超越。', judgment: '栋桡利有攸往亨', judgmentMeaning: '房屋的栋梁弯曲，利于前往，亨通' },
    29: { name: '坎', latin: 'Kan', english: 'Abyss', gua: '䷜', meaning: '象征坎陷，水坎。代表危险与陷阱。', content: '习坎有孚维心亨行有尚', meaning: '重坎而有诚信，维系中心，亨通' },
    30: { name: '离', latin: 'Li', english: 'Clinging', gua: '䷝', meaning: '象征火焰，离为火。代表依附与明丽。', judgment: '亨畜牝牛吉', judgmentMeaning: '亨通，畜养母牛吉祥' },
    31: { name: '咸', latin: 'Xian', english: 'Resonance', gua: '䷞', meaning: '象征感应，山泽咸。代表相互感应。', judgment: '亨利贞取女吉', judgmentMeaning: '亨通利于正固，取女吉祥' },
    32: { name: '恒', latin: 'Heng', english: 'Constancy', gua: '䷟', meaning: '象征恒久，雷风恒。代表永恒与持续。', judgment: '亨无咎利贞利有攸往', judgmentMeaning: '亨通没有灾祸，利于正固' },
    33: { name: '遁', latin: 'Dun', english: 'Retreat', gua: '䷠', meaning: '象征退隐，天山遁。代表退避与隐遁。', judgment: '亨小利贞', judgmentMeaning: '亨通，稍微有利' },
    34: { name: '大壮', latin: 'Da Zhuang', english: 'Great Strength', gua: '䷡', meaning: '象征壮大，雷天大壮。代表强盛与壮大。', judgment: '利贞', judgmentMeaning: '利于正固' },
    35: { name: '晋', latin: 'Jin', english: 'Advance', gua: '䷢', meaning: '象征前进，火地晋。代表晋升与进益。', judgment: '康侯用锡马蕃庶昼日三接', judgmentMeaning: '康侯得到很多马，一天三次接见' },
    36: { name: '明夷', latin: 'Ming Yi', english: 'Darkness', gua: '䷣', meaning: '象征光明受伤，地火明夷。代表蒙难与晦暗。', judgment: '利艰贞', judgmentMeaning: '利于艰难中正固' },
    37: { name: '家人', latin: 'Jia Ren', english: 'Family', gua: '䷤', meaning: '象征家人，风火家人。代表家庭与治家。', judgment: '利女贞', judgmentMeaning: '利于女子正固' },
    38: { name: '睽', latin: 'Kui', english: 'Opposition', gua: '䷥', meaning: '象征乖睽，火泽睽。代表对立与分歧。', judgment: '小事吉', judgmentMeaning: '小事吉祥' },
    39: { name: '蹇', latin: 'Jian', english: 'Obstruction', gua: '䷦', meaning: '象征艰难，水山蹇。代表阻难与困苦。', judgment: '利西南不利东北利见大人贞吉', judgmentMeaning: '利于西南，不利于东北' },
    40: { name: '解', latin: 'Jie', english: 'Release', gua: '䷧', meaning: '象征解除，雷水解。代表解脱与缓解。', judgment: '利西南无所往其来复吉有攸往夙吉', judgmentMeaning: '利于西南，返回吉祥' },
    41: { name: '损', latin: 'Sun', english: 'Decrease', gua: '䷨', meaning: '象征减损，山泽损。代表损失与奉献。', judgment: '有孚元吉无咎可贞利有攸往曷之用二簋可用亨', judgmentMeaning: '心怀诚信，大吉无灾' },
    42: { name: '益', latin: 'Yi', english: 'Increase', gua: '䷩', meaning: '象征增益，风雷益。代表增长与受益。', judgment: '利有攸往利涉大川', judgmentMeaning: '利于前往，利于渡过大河' },
    43: { name: '夬', latin: 'Guai', english: 'Resolution', gua: '䷪', meaning: '象征决断，泽天夬。代表果断与决裂。', judgment: '扬于王庭孚号有厉告自邑不利即戎利有攸往', judgmentMeaning: '在王庭宣扬，有危险报告' },
    44: { name: '姤', latin: 'Gou', english: 'Meeting', gua: '䷫', meaning: '象征相遇，天风姤。代表邂逅与机遇。', judgment: '女壮勿用取女', judgmentMeaning: '女子强壮，不宜娶女' },
    45: { name: '萃', latin: 'Cui', english: 'Gathering', gua: '䷬', meaning: '象征聚集，泽地萃。代表聚合与团结。', judgment: '亨王假有庙利见大人亨利贞用大牲吉利有攸往', judgmentMeaning: '亨通，王到庙里，利于见大人' },
    46: { name: '升', latin: 'Sheng', english: 'Ascending', gua: '䷭', meaning: '象征上升，地风升。代表晋升与发展。', judgment: '元亨用见大人勿恤南征吉', judgmentMeaning: '大亨通，见大人无需忧虑' },
    47: { name: '困', latin: 'Kun', english: 'Exhaustion', gua: '䷮', meaning: '象征困穷，泽水困。代表困境与磨难。', judgment: '亨贞大人吉无咎有言不信', judgmentMeaning: '亨通正固，大人吉祥无灾' },
    48: { name: '井', latin: 'Jing', english: 'Well', gua: '䷯', meaning: '象征水井，风水井。代表取之不尽。', judgment: '改邑不改井无丧无得往来井井汔至亦未繘井羸其瓶凶', judgmentMeaning: '改变城邑而不改变井' },
    49: { name: '革', latin: 'Ge', english: 'Revolution', gua: '䷰', meaning: '象征变革，泽火革。代表改革与改变。', judgment: '己日乃孚元亨利贞悔亡', judgmentMeaning: '己日才有诚信，大亨通，正固' },
    50: { name: '鼎', latin: 'Ding', english: 'Cauldron', gua: '䷱', meaning: '象征鼎器，火风鼎。代表权威与稳定。', judgment: '元吉亨', judgmentMeaning: '大吉祥亨通' },
    51: { name: '震', latin: 'Zhen', english: 'Thunder', gua: '䷲', meaning: '象征雷震，震为雷。代表震动与警醒。', judgment: '亨震来虩虩笑言哑哑震惊百里不丧匕鬯', judgmentMeaning: '雷声来临，笑声不断' },
    52: { name: '艮', latin: 'Gen', english: 'Stopping', gua: '䷳', meaning: '象征停止，山艮。代表静止与限制。', judgment: '艮其背不获其身行其庭不见其人无咎', judgmentMeaning: '止于背部，不能获得身体' },
    53: { name: '渐', latin: 'Jian', english: 'Progress', gua: '䷴', meaning: '象征渐进，风山渐。代表循序渐进。', judgment: '女归吉利贞', judgmentMeaning: '女子出嫁吉祥正固' },
    54: { name: '归妹', latin: 'Gui Mei', english: 'Marrying', gua: '䷵', meaning: '象征归妹，雷泽归妹。代表婚姻与归宿。', judgment: '征凶无攸利', judgmentMeaning: '前往有凶险，无所利' },
    55: { name: '丰', latin: 'Feng', english: 'Abundance', gua: '䷶', meaning: '象征丰盛，雷火丰。代表丰盈与盛大。', judgment: '亨王假之勿忧宜日中', judgmentMeaning: '王到来，不要忧虑，宜在日中' },
    56: { name: '旅', latin: 'Lu', english: 'Travel', gua: '䷷', meaning: '象征旅行火山旅。代表漂泊与羁旅。', judgment: '小亨旅贞吉', judgmentMeaning: '稍微亨通，旅行正固吉祥' },
    57: { name: '巽', latin: 'Xun', english: 'Wind', gua: '䷸', meaning: '象征顺从，风为巽。代表柔顺与进入。', judgment: '小亨利有攸往利见大人', judgmentMeaning: '稍微亨通，利于前往' },
    58: { name: '兑', latin: 'Dui', english: 'Joy', gua: '䷹', meaning: '象征喜悦，泽为兑。代表愉悦与和谈。', judgment: '亨利贞', judgmentMeaning: '亨通利于正固' },
    59: { name: '涣', latin: 'Huan', english: 'Dispersion', gua: '䷺', meaning: '象征涣散风水涣。代表离散与疏通。', judgment: '王假有庙利涉大川利贞', judgmentMeaning: '王到庙里，利于渡大河' },
    60: { name: '节', latin: 'Jie', english: 'Limitation', gua: '䷻', meaning: '象征节制，水泽节。代表限制与节约。', judgment: '亨苦节不可贞', judgmentMeaning: '亨通，过分节制不可正固' },
    61: { name: '中孚', latin: 'Zhong Fu', english: 'Inner Truth', gua: '䷼', meaning: '象征诚信，风泽中孚。代表真诚与信用。', judgment: '豚鱼吉利涉大川利贞', judgmentMeaning: '小猪和鱼吉祥，利于渡大河' },
    62: { name: '小过', latin: 'Xiao Guo', english: 'Small Exceeding', gua: '䷽', meaning: '象征小过，雷山小过。代表稍有过度。', judgment: '亨利贞可小事不可大事飞鸟遗之音不宜上宜下大吉', judgmentMeaning: '亨通利于正固，可以做小事' },
    63: { name: '未济', latin: 'Wei Ji', english: 'Not Yet', gua: '䷾', meaning: '象征未济，火水未济。代表尚未完成。', judgment: '亨小狐汔济濡其尾无攸利', judgmentMeaning: '亨通，小狐几乎渡过' },
    64: { name: '既济', latin: 'Ji Ji', english: 'Already', gua: '䷿', meaning: '象征既济，水火既济。代表已完成。', judgment: '亨小利贞初吉终乱', judgmentMeaning: '亨通稍微有利正固' }
};

// 变爻解释
const changingLines = {
    1: '初九：潜龙勿用。\n九二：见龙在田，利见大人。\n九三：君子终日乾乾，夕惕若厉，无咎。\n九四：或跃在渊，无咎。\n九五：飞龙在天，利见大人。\n上九：亢龙有悔。\n用九：见群龙无首，吉。',
    2: '初六：履霜，坚冰至。\n六二：直方大，不习无不利。\n六三：含章可贞，或从王事，无成有终。\n六四：括囊，无咎无誉。\n六五：黄裳，元吉。\n上六：龙战于野，其血玄黄。\n用六：利永贞。'
};

// 三枚铜钱占卜
function tossCoins() {
    // 1为阳，0为阴
    // 三枚铜钱，正面(1)记为3，反面(0)记为2
    // 三次结果相加：6(少阴)、7(少阳)、8(老阴)、9(老阳)
    const results = [];
    for (let i = 0; i < 3; i++) {
        const toss = Math.random() < 0.5 ? 2 : 3;
        results.push(toss);
    }
    return results.reduce((a, b) => a + b, 0);
}

// 生成卦象
function generateHexagram() {
    const gua = [];
    for (let i = 0; i < 6; i++) {
        gua.push(tossCoins());
    }
    return gua;
}

// 判断变爻
function getChangingLines(gua) {
    const changing = [];
    gua.forEach((value, index) => {
        if (value === 6 || value === 9) {
            changing.push(index + 1);
        }
    });
    return changing;
}

// API: 获取新卦象
app.post('/api/divination', (req, res) => {
    const { question } = req.body;
    const gua = generateHexagram();
    const changing = getChangingLines(gua);
    
    // 计算主卦和变卦
    const mainHex = gua.map(v => v >= 7 ? 1 : 0);
    const changedHex = gua.map(v => {
        if (v === 6) return 1; // 老阴变阳
        if (v === 9) return 0; // 老阳变阴
        return v >= 7 ? 1 : 0;
    });
    
    // 计算卦数
    const mainNumber = gua.filter(v => v === 7 || v === 9).length;
    const changedNumber = gua.filter(v => v === 6 || v === 9).length;
    
    res.json({
        success: true,
        gua,
        changing,
        mainHex,
        changedHex,
        mainNumber,
        changedNumber,
        question
    });
});

// API: 获取卦象详情
app.get('/api/hexagram/:id', (req, res) => {
    const id = parseInt(req.params.id);
    if (hexagrams[id]) {
        res.json({
            success: true,
            ...hexagrams[id]
        });
    } else {
        res.json({ success: false, message: '卦象不存在' });
    }
});

// API: 获取所有卦象列表
app.get('/api/hexagrams', (req, res) => {
    const list = Object.entries(hexagrams).map(([id, data]) => ({
        id: parseInt(id),
        name: data.name,
        english: data.english,
        gua: data.gua
    }));
    res.json({ success: true, list });
});

// 启动服务器
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`易经占卜服务器运行在 http://localhost:${PORT}`);
});
