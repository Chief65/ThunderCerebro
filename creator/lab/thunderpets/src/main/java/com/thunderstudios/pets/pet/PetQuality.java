package com.thunderstudios.pets.pet;

public enum PetQuality {
    SUPER(" &8⁂ &#4BFD00&lS&#47F504&lU&#44EC08&lP&#40E40C&lE&#3CDB10&lR &e⭐&7⭐⭐⭐⭐", "&#3CDB10", 20),
    RARA(" &8⁂ &#008DFF&lR&#0AA1FF&lA&#13B4FF&lR&#1DC8FF&lA &e⭐⭐&7⭐⭐⭐", "&#1DC8FF", 40),
    EPICA(" &8⁂ &#A84EDE&lE&#9B45DF&lP&#8E3CE0&lI&#8033E1&lC&#732AE2&lA &e⭐⭐⭐&7⭐⭐", "&#732AE2", 60),
    MITICA(" &8⁂ &#B01111&lM&#B61515&lI&#BD1919&lT&#C31E1E&lI&#CA2222&lC&#D02626&lA &e⭐⭐⭐⭐&7⭐", "&#D02626", 80),
    DIVINA(" &8⁂ &#FD9A00&lD&#FAAE00&lI&#F7C200&lV&#F5D700&lI&#F2EB00&lN&#EFFF00&lA &e⭐⭐⭐⭐⭐", "&#EFFF00", 100),
    LIMITED(" &8⁂ &#FF4B4B&l¡&#FF8B2D&lL&#FFD031&lI&#DCFF39&lM&#A5FF3F&lI&#6DFF45&lT&#3BFFC7&lE&#58D0FF&lD&#5489FF&l! &#FD9A00&m⭐&#FAB300&m⭐&#F6CD00&m⭐&#F3E600&m⭐&#EFFF00&m⭐", "&#5489FF", 120);

    private final String canonTag;
    private final String nameColor;
    private final int maxLevel;

    PetQuality(String canonTag, String nameColor, int maxLevel) {
        this.canonTag = canonTag;
        this.nameColor = nameColor;
        this.maxLevel = maxLevel;
    }

    public String getCanonTag() { return canonTag; }
    public String getNameColor() { return nameColor; }
    public int getMaxLevel() { return maxLevel; }

    public static PetQuality fromString(String str) {
        if (str == null) return SUPER;
        try {
            return valueOf(str.toUpperCase());
        } catch (Exception e) {
            return SUPER;
        }
    }
}
