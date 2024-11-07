class MealsListData {
  MealsListData({
    this.imagePath = '',
    this.titleTxt = '',
    this.startColor = '',
    this.endColor = '',
    this.meals,
    this.kacl = 0,
  });

  String imagePath;
  String titleTxt;
  String startColor;
  String endColor;
  List<String>? meals;
  int kacl;

  static List<MealsListData> tabIconsList = <MealsListData>[
    MealsListData(
      imagePath: 'assets/fitness_app/key.png',
      titleTxt: '계정',
      // kacl: 525,
      meals: <String>['계정 정보'],
      startColor: '#FA7D82',
      endColor: '#FFB295',
    ),
    MealsListData(
      imagePath: 'assets/fitness_app/question.png',
      titleTxt: '문의하기',
      // kacl: 602,
      meals: <String>['궁금하신 걸','물어보세요'],
      startColor: '#738AE6',
      endColor: '#5C5EDD',
    ),
    MealsListData(
      imagePath: 'assets/fitness_app/info.png',
      titleTxt: '도움말',
      // kacl: 0,
      meals: <String>['앱에 관한 정보'],
      startColor: '#FE95B6',
      endColor: '#FF5287',
    ),
  ];
}
